import asyncio
import json
import git


import requests
import os 
import zipfile
import logging
import shutil
from bs4 import BeautifulSoup
import aiohttp
import re

FULL_LIST= "https://models.physiomeproject.org/exposure/listing/full-list"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)





async def importProjects():
    """
    Imports all the projects in the database
    """
    projectExposureLinks = await getProjectsList()
    numProjects = len(projectExposureLinks)
    
    async with aiohttp.ClientSession() as session:
        shutil.rmtree("projects", ignore_errors=True)

        # various hrefs for the project
        project_urls_task = []


        for project in projectExposureLinks:
            #logger.debug(f'Importing {project}')
            projectName= project.split('/')[-1]
            os.makedirs(f'projects/{projectName}', exist_ok=True)
            project_urls_task.append(getProjectHrefs(session, project))
        
        projectLinks = await asyncio.gather(*project_urls_task, return_exceptions=True)

        # Combine archive download for each project
        archive_tasks = []
        # Extract the metadata we can from each project
        metadata_tasks = []
        # Get the entire workspace for each project
        workspace_tasks = []

        for projectlink in projectLinks:
            
            projectName = projectlink['project'].split('/')[-1]
            
            archive_tasks.append(asyncio.ensure_future(getProjectArchive(session, projectlink['archive'])))
            
            workspace_tasks.append(getProjectWorkspace(projectName, projectlink['workspace']))
            

            metadata_tasks.append(asyncio.ensure_future(getProjectInfo(session, projectlink['project'], projectlink['documentation'], projectlink['metadata'])))

        try:
            archives = await asyncio.gather(*archive_tasks, return_exceptions=True)
            workspaces = await asyncio.gather(*workspace_tasks, return_exceptions=True)
            metadata = await asyncio.gather(*metadata_tasks, return_exceptions=True)

        except Exception as e:
            logger.error(e)
                    
        projectNames = [projectlink['project'].split('/')[-1] for projectlink in projectLinks]
        failed_project_archive_download= [ projectNames[index] for index, archive in enumerate(archives) if isinstance(archive, Exception)]
        if(len(failed_project_archive_download) > 0):
            logger.error(f'Failed to download project archives: {failed_project_archive_download}')

        failed_project_workspace_download= [ projectNames[index] for index, workspace in enumerate(workspaces) if isinstance(workspace, Exception)]
        if(len(failed_project_workspace_download) > 0):
            logger.error(f'Failed to download project workspaces: {failed_project_workspace_download}')

        failed_project_metadata_download= [ projectNames[index] for index, metadata in enumerate(metadata) if isinstance(metadata, Exception)]
        if(len(failed_project_metadata_download) > 0):
            logger.error(f'Failed to download project metadata: {failed_project_metadata_download}')
            metadata= [value if not isinstance(value, Exception) else repr(value) for value in metadata]
        
        projectMetadatas= dict(zip(projectNames, metadata))
        
        with open('projects.json', 'w') as f:
            json.dump(projectMetadatas, f)
        
        
        

        logger.debug(f'Got {len(archives)- len(failed_project_archive_download)} archives')
        logger.debug(f'Got {len(workspaces)- len(failed_project_workspace_download)} workspaces')
        logger.debug(f'Got {len(metadata)- len(failed_project_metadata_download)} metadata')

            


async def getProjectHash(session, link):
    """
    Returns the hash of the project
    """
    async with session.get(link, headers={'Accept': 'application/json'}) as resp:
        req = await resp.json()
        return req['project']['hash']

async def getProjectArchive(session, link):
        
    name= link.split('/')[-2]
    
    async with session.get(link, headers={'Accept': 'application/zip'}) as resp:

        archive = await resp.read()
        with open(f'projects/{name}/{name}.omex', 'wb') as f:
            f.write(archive)
        
        with zipfile.ZipFile(f'projects/{name}/{name}.omex') as zf:
            zf.extractall(f'projects/{name}/omexContents')
        return True
        
  

async def getProjectsList():
    """
    Returns a list of all the projects in the database
    """
    
    async with aiohttp.ClientSession() as session:
        async with session.get(FULL_LIST,headers={'Accept': 'application/json'}) as resp:
            req = await resp.json()
            
            links =req['collection']['links']
            links=  list(map(lambda x: x['href'], links)) 
            
            return links[:]
        

async def getProjectHrefs(session, projectExposureHref):
    """
    Returns the hrefs for the project
    """
    async with session.get(projectExposureHref, headers={'Accept': 'application/json'}) as resp:
        links ={
            'project': projectExposureHref,
            'archive': f'{projectExposureHref}/download_generated_omex',
            'workspace': None,
            'documentation': None,
            'metadata': None,            

        }
        req = await resp.json()
        req= req['collection']['links']
        for link in req:
            if link['prompt'] == 'Workspace URL':
                links['workspace'] = link['href']
                break
        for link in req:
            if link['href'].endswith('.cellml/view'):
                links['documentation'] = link['href']
                links['metadata'] = link['href'].replace('.cellml/view', '.cellml/cmeta')                
                break
                
        return links
        
async def getProjectWorkspace(name, link):
    """
    Saves the workspace for the project
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, git.Repo.clone_from, link, f'projects/{name}/workspace')
    return True
    



async def getProjectInfo(session, project_href, documentation_href, metadata_href):
    """
    
    """

    model_metadata = {
        "identifier": "",
        "hash": "",
        "title": None,
        "description": None,
        "authors": None,
        "license": None,
        "thumbnails": [],
        "tags": [],
        "created": None,
        "modified": None,
        "citation": [],
        "contributor": "Bilal Shaikh",
        "errors": [],
    }
    if(project_href):
        async with session.get(project_href, headers={'Accept': 'application/json'}) as resp:
            try: 
                req = await resp.json()
                model_metadata['identifier'] = project_href.split('/')[-1]    
                data= req['collection']['items'][0]['data']

                for item in data:
                    if item['name'] == 'title':
                        model_metadata['title'] = item['value']
                    if item["name"] == "commit_id":
                        model_metadata['hash'] = item['value']
            except Exception as e:
                model_metadata['errors'].append(repr(e))
    else:
        model_metadata['errors'].append('No project href')

    if(documentation_href):
        async with session.get(documentation_href, headers={'Accept': 'text/html'}) as resp:
            
            try:
                html_page = (await resp.text())
                if(html_page):
                    soup = BeautifulSoup(html_page, 'html.parser')
                    # Get the metadata from the page
                    image= soup.find("img", class_="tmp-doc-informalfigure")
                    image_url = documentation_href + image['src']

                    model_metadata['thumbnails'].append(image_url)
                    description = soup.find("div", id="content-core").find_all(re.compile("[hp]"))
                    description = [x.get_text() for x in description]
                    
                    model_metadata['description'] = '\n'.join(description)
            except Exception as e:
                model_metadata['errors'].append(repr(e))
    else:
        model_metadata['errors'].append('No documentation href')
                
            
    if(metadata_href):
        async with session.get(metadata_href, headers={'Accept': 'application/json'}) as resp:
            try:
                req= await resp.json()
                metadatas= req['collection']['items'][0]['data']
                for metadata in metadatas:
                    if metadata['name'] == 'keywords':
                        model_metadata['tags'] = metadata['value']
                    if metadata['name'] == 'citation_title':
                        model_metadata['citation'].append(metadata['value'])
                    if metadata['name'] == 'citation_authors':
                        model_metadata['citation'].append(metadata['value'])
                    if metadata['name'] == 'citation_journal':
                        model_metadata['citation'].append(metadata['value'])
                    if metadata['name'] == 'citation_id':
                        model_metadata['citation'].append(metadata['value'])
                    if metadata['name'] == 'model_author':
                        model_metadata['authors'] = metadata['value']
            except(Exception) as e:
                model_metadata['errors'].append(repr(e))
    else:
        model_metadata['errors'].append('No metadata href')

            
    return model_metadata
        

 
    
