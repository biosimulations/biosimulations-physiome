import asyncio
from cmath import pi
from curses import meta
from importlib.metadata import metadata
import json
import os
import zipfile
import logging
import shutil
from bs4 import BeautifulSoup
import aiohttp
import re


FULL_LIST = "https://models.physiomeproject.org/exposure/listing/full-list"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)


async def importProjects(startAt=0, endAt=-1, getWorkspaces=True, getMetadata=True):
    """
    Imports all the projects in the database
    """
    logger = logging.getLogger(__name__)
    projectExposureLinks = await getProjectsList(startAt, endAt)
    numProjects = len(projectExposureLinks)

    async with aiohttp.ClientSession() as session:

        # various hrefs for the project
        project_urls_task = []

        for project in projectExposureLinks:
            logger.debug(f'Getting Links for {project}')
            projectName = project.split('/')[-1]
            os.makedirs(f'projects/{projectName}', exist_ok=True)
            project_urls_task.append(getProjectHrefs(session, project))

        projectLinks = await asyncio.gather(*project_urls_task, return_exceptions=False)
        print(projectLinks)
        with open('projectLinks.json', 'w') as f:
            json.dump(projectLinks, f, indent=4)
        # Extract the metadata we can from each project
        metadata_tasks = []
        all_tasks = []
        archives = []
        metadata = []
        workspaces = []
        exit()
        for projectlink in projectLinks:

            projectName = projectlink['project'].split('/')[-1]
            if(getMetadata):
                metadata_tasks.append(asyncio.ensure_future(getProjectInfo(
                    session, projectlink)))

        # Metadata for each project
        metadata = await asyncio.gather(*metadata_tasks, return_exceptions=True)

        # have to do this synchronously because otherwise we seem to be overloading the pmr git server
        if(getWorkspaces):
            getGitRepos(projectLinks)

        with open('projects.json', 'w') as f:
            json.dump(metadata, f, indent=4)


async def getProjectHash(session, link):
    """
    Returns the hash of the project
    """
    async with session.get(link, headers={'Accept': 'application/json'}) as resp:
        req = await resp.json()
        return req['project']['hash']


async def getProjectsList(startAt=0, endAt=-1):
    """
    Returns a list of all the projects in the database
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(FULL_LIST, headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting full list of projects')
            req = await resp.json()

            links = req['collection']['links']
            links = list(map(lambda x: x['href'], links))

            return links[startAt:endAt]


async def getProjectHrefs(session, projectExposureHref):
    """
    Returns the hrefs for the project
    """
    async with session.get(projectExposureHref, headers={'Accept': 'application/json'}) as resp:

        created_project_links = {
            'project': projectExposureHref,
            'workspace': None,
            'content': [],

        }
        exposure_info = await resp.json()
        print("response for project: ", projectExposureHref)
        
        exposure_links = exposure_info['collection']['links']
        # Handle this weirdness for  PMR2/pmr2.app#6
        if(projectExposureHref == "https://models.physiomeproject.org/exposure/e340f005288ec6bd49535cf792769dd0"):
            exposure_links= []
        for exposure_link in exposure_links:
            if exposure_link['prompt'] == 'Workspace URL':
                created_project_links['workspace'] = exposure_link['href']
            if exposure_link['rel'] == "bookmark":
                file_prompt = exposure_link['prompt']
                file_link = exposure_link['href']
                async with session.get(file_link, headers={'Accept': 'application/json'}) as fileInfo:
                    try:
                        file_info = await fileInfo.json()
                    except aiohttp.ContentTypeError as e:
                        print("Failure to get file info for: ", projectExposureHref)
                        print(exposure_info)
                        print("Failed to parse json for file: ", file_link)
                        raise e

                    file_name = file_link.split('/')[-2]
                    created_file_links = {
                        'title': None,
                        'file_name': file_name,
                        'href': file_link,
                        'file_type': None,
                        'documentation': None,
                        'metadata': None}

                    for data in file_info['collection']['items'][0]['data']:
                        if data['name'] == 'title':
                            created_file_links['title'] = data['value']
                        if data['name'] == 'file_type':
                            created_file_links['file_type'] = data['value']

                    for link in file_info['collection']['links']:
                        if link['prompt'] == 'Documentation':
                            created_file_links['documentation'] = link['href']
                        if link['prompt'] == 'Model Metadata':
                            created_file_links['metadata'] = link['href']
                    created_project_links['content'].append(created_file_links)

        return created_project_links


def getGitRepos(projectLinks):
    success = []
    for projectLink in projectLinks:
        projectName = projectLink['project'].split('/')[-1]
        success.append(getGitRepo(projectName, projectLink['workspace']))

    # Delete all the .git folders and .gitmodules files to prevent issues with top level git repo
    logger.debug(f'Deleting .git folders and .gitmodules files')
    os.system('find . -type d -name ".git" -ls -exec rm -rvf {} +')
    os.system('find . -type f -name ".git" -ls -exec rm -rvf {} +')
    os.system('find . -type f -name ".gitmodules" -delete')


def getGitRepo(name, link):
    logger.debug(f'Getting git repo for {name}')
    shutil.rmtree(f'projects/{name}/workspace', ignore_errors=True)

    if(link):
        try:
            logger.info(f'Cloning {name}')
            os.system(
                f'git clone --recurse-submodules {link} projects/{name}/workspace ')
            shutil.rmtree(
                f'projects/{name}/workspace/.git', ignore_errors=True)
            shutil.rmtree(
                f'projects/{name}/workspace/.gitmodules', ignore_errors=True)
        except Exception as e:
            logger.error(e)
            return False

    return True


async def getProjectInfo(session, projectlink):
    """

    """
    project_href, documentation_href, metadata_href, workspace_href = projectlink[
        'project'], projectlink['documentation'], projectlink['metadata'], projectlink['workspace']
    projectName = project_href.split('/')[-1]

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
                data = req['collection']['items'][0]['data']

                for item in data:
                    if item['name'] == 'title':
                        model_metadata['title'] = (item['value'] or "").strip()
                    if item["name"] == "commit_id":
                        model_metadata['hash'] = item['value']
            except Exception as e:
                logger.error(
                    f'Failed to get project info for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))
                raise
    else:
        logger.error(
            f'Failed to get project info for {projectName} due to missing project href')
        model_metadata['errors'].append('No project href')

    if(documentation_href):
        async with session.get(documentation_href, headers={'Accept': 'text/html'}) as resp:
            logger.debug(f'Getting documentation for {projectName}')
            try:
                html_page = (await resp.text())
                if(html_page):
                    soup = BeautifulSoup(html_page, 'html.parser')
                    # Get the metadata from the page
                    image = soup.find("img", class_="tmp-doc-informalfigure")
                    if(image):
                        image_url = documentation_href + "/" + image['src']
                        model_metadata['thumbnails'].append(image_url)
                    description = soup.find(
                        "div", id="content-core").find_all(re.compile("[hp]"))
                    description = [x.get_text() for x in description]

                    model_metadata['description'] = '\n'.join(description)
            except Exception as e:
                logger.error(
                    f'Failed to get documentation for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))

    else:
        logger.error(
            f'Failed to get documentation for {projectName} due to missing documentation href')
        model_metadata['errors'].append('No documentation href')

    if(metadata_href):
        async with session.get(metadata_href, headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting metadata for {projectName}')
            try:
                req = await resp.json()
                metadatas = req['collection']['items'][0]['data']
                for metadata in metadatas:
                    if metadata['name'] == 'keywords':
                        model_metadata['tags'] = metadata['value']
                    if metadata['name'] == 'citation_title':
                        model_metadata['citation']['title'] = metadata['value']
                    if metadata['name'] == 'citation_authors':
                        model_metadata['citation']["authors"] = metadata['value']
                    if metadata['name'] == 'citation_journal':
                        model_metadata['citation']['journal'] = metadata['value']
                    if metadata['name'] == 'citation_id':
                        model_metadata['citation']['identifier'] = metadata['value']
                    if metadata['name'] == 'model_author':
                        model_metadata['authors'] = metadata['value']
            except(Exception) as e:
                logger.error(
                    f'Failed to get metadata for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))

    else:
        logger.error(
            f'Failed to get metadata for {projectName} due to missing metadata href')
        model_metadata['errors'].append('No metadata href')

    return model_metadata
