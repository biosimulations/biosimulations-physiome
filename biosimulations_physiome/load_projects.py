import asyncio
from curses import meta
import json
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
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)




async def importProjects(clearProjects=False, startAt=0, endAt=-1, getWorkspaces=True, getMetadata=True, getArchives=True):
    """
    Imports all the projects in the database
    """
    logger= logging.getLogger(__name__)
    projectExposureLinks = await getProjectsList(startAt, endAt)
    numProjects = len(projectExposureLinks)
    
    if(clearProjects):
        shutil.rmtree('projects', ignore_errors=True)
    
    async with aiohttp.ClientSession() as session:
        

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
        all_tasks = []
        archives= []
        metadata= []
        workspaces= []
        for projectlink in projectLinks:
            
            projectName = projectlink['project'].split('/')[-1]
            if(getArchives):
                archive_tasks.append(asyncio.ensure_future(getProjectArchive(session, projectlink['archive'])))
            
            if(getMetadata):
                metadata_tasks.append(asyncio.ensure_future(getProjectInfo(session, projectlink['project'], projectlink['documentation'], projectlink['metadata'], projectLink['workspace'])))

        
        all_tasks = await asyncio.gather(*archive_tasks, *metadata_tasks, return_exceptions=True)  
        if(getArchives):
            archives = all_tasks[:numProjects]
        if(getMetadata and getArchives):
            metadata = all_tasks[numProjects:]
        if(getMetadata and not getArchives):
            metadata = all_tasks
        # have to do this synchronously because otherwise we seem to be overloading the pmr git server
        if(getWorkspaces):
            for projectLink in projectLinks:
                projectName = projectLink['project'].split('/')[-1]
                getGitRepo(projectName, projectLink['workspace'])
            # Delete all the .git folders and .gitmodules files to prevent issues with top level git repo
            os.system('find . -type d -name ".git" -delete')
            os.system('find . -type f -name ".gitmodules" -delete')

                
            
        



        projectNames = [projectlink['project'].split('/')[-1] for projectlink in projectLinks]
        failed_project_archive_download= [ projectNames[index] for index, archive in enumerate(archives) if isinstance(archive, Exception)]
        if(len(failed_project_archive_download) > 0):
            logger.error(f'Failed to download project archives: {failed_project_archive_download}')

        failed_project_workspace_download= [ (projectNames[index], repr(workspace)) for index, workspace in enumerate(workspaces) if isinstance(workspace, Exception)]
        if(len(failed_project_workspace_download) > 0):
            logger.error(f'Failed to download project workspaces: {failed_project_workspace_download}')

        failed_project_metadata_download= [ projectNames[index] for index, metadata in enumerate(metadata) if isinstance(metadata, Exception)]
        if(len(failed_project_metadata_download) > 0):
            logger.error(f'Failed to download project metadata: {failed_project_metadata_download}')
            metadata= [value if not isinstance(value, Exception) else repr(value) for value in metadata]
        
        projectMetadatas= dict(zip(projectNames, metadata))
        
        logger.info(f'Imported {numProjects} projects')
        logger.info(f'Saving metadata to projects.json')
        with open('projects.json', 'w') as f:
            json.dump(metadata, f)    
        
        

        logger.info(f'Got {len(archives)- len(failed_project_archive_download)}/{len(archives)} archives')
        logger.info(f'Got {len(workspaces)- len(failed_project_workspace_download)}/{len(workspaces)} workspaces')
        logger.info(f'Got {len(metadata)- len(failed_project_metadata_download)}/{len(metadata)} metadata')

            


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
        logger.debug(f'Downloading {name} omex archive')
        archive = await resp.read()
        with open(f'projects/{name}/{name}.omex', 'wb') as f:
            f.write(archive)
        logger.debug(f'Extracting {name} omex archive')
        with zipfile.ZipFile(f'projects/{name}/{name}.omex') as zf:
            zf.extractall(f'projects/{name}/omexContents')
        return True
        
  

async def getProjectsList(startAt=0, endAt=-1):
    """
    Returns a list of all the projects in the database
    """
    
    async with aiohttp.ClientSession() as session:
        async with session.get(FULL_LIST,headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting full list of projects')
            req = await resp.json()
            
            links =req['collection']['links']
            links=  list(map(lambda x: x['href'], links)) 
            
            return links[startAt:endAt]
        

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
        
def getGitRepo(name, link):
    logger.debug(f'Getting git repo for {name}')    
    shutil.rmtree(f'projects/{name}/workspace', ignore_errors=True)

    if(link):
        try:
            logger.info(f'Cloning {name}')
            os.system(f'git clone --recurse-submodules {link} projects/{name}/workspace ')
            shutil.rmtree(f'projects/{name}/workspace/.git', ignore_errors=True)
            shutil.rmtree(f'projects/{name}/workspace/.gitmodules', ignore_errors=True)
        except Exception as e:
                logger.error(e)
                return False   

    
    
    return True
    
    



async def getProjectInfo(session, project_href, documentation_href, metadata_href, workspace_href):
    """
    
    """
    projectName= project_href.split('/')[-1]
    
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
        "source": workspace_href,
        "citation": {
            "title": None,
            "authors": None,
            "journal": None,
            "identifier": None,
        },
        "contributor": "Bilal Shaikh",
        "errors": [],
    }
    if(project_href):
        async with session.get(project_href, headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting project info for {project_href}')
            try: 
                req = await resp.json()
                model_metadata['identifier'] = project_href.split('/')[-1]    
                data= req['collection']['items'][0]['data']

                for item in data:
                    if item['name'] == 'title':
                        model_metadata['title'] = (item['value'] or "").strip()
                    if item["name"] == "commit_id":
                        model_metadata['hash'] = item['value']
            except Exception as e:
                logger.error(f'Failed to get project info for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))
                raise
    else:
        logger.error(f'Failed to get project info for {projectName} due to missing project href')
        model_metadata['errors'].append('No project href')

    if(documentation_href):
        async with session.get(documentation_href, headers={'Accept': 'text/html'}) as resp:
            logger.debug(f'Getting documentation for {projectName}')
            try:
                html_page = (await resp.text())
                if(html_page):
                    soup = BeautifulSoup(html_page, 'html.parser')
                    # Get the metadata from the page
                    image= soup.find("img", class_="tmp-doc-informalfigure")
                    if(image):
                        image_url = documentation_href+ image['src']
                        model_metadata['thumbnails'].append(image_url)
                    description = soup.find("div", id="content-core").find_all(re.compile("[hp]"))
                    description = [x.get_text() for x in description]
                    
                    model_metadata['description'] = '\n'.join(description)
            except Exception as e:
                logger.error(f'Failed to get documentation for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))
                
    else:
        logger.error(f'Failed to get documentation for {projectName} due to missing documentation href')
        model_metadata['errors'].append('No documentation href')
                
            
    if(metadata_href):
        async with session.get(metadata_href, headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting metadata for {projectName}')
            try:
                req= await resp.json()
                metadatas= req['collection']['items'][0]['data']
                for metadata in metadatas:
                    if metadata['name'] == 'keywords':
                        model_metadata['tags'] = metadata['value']
                    if metadata['name'] == 'citation_title':
                        model_metadata['citation']['title'] =metadata['value']
                    if metadata['name'] == 'citation_authors':
                        model_metadata['citation']["authors"] = metadata['value']
                    if metadata['name'] == 'citation_journal':
                        model_metadata['citation']['journal'] =metadata['value'] 
                    if metadata['name'] == 'citation_id':
                        model_metadata['citation']['identifier'] = metadata['value']
                    if metadata['name'] == 'model_author':
                        model_metadata['authors'] = metadata['value']
            except(Exception) as e:
                logger.error(f'Failed to get metadata for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))
                
    else:
        logger.error(f'Failed to get metadata for {projectName} due to missing metadata href')
        model_metadata['errors'].append('No metadata href')

    return model_metadata
        

 
    
