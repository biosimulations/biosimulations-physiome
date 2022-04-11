from ast import mod
import asyncio
from cmath import pi
from curses import meta
from os.path import exists

import json
import os
from time import sleep
import shutil
from bs4 import BeautifulSoup
import aiohttp
from aiohttp_client_cache import CachedSession, FileBackend, SQLiteBackend
from loguru import logger
import markdownify
FULL_LIST = "https://models.physiomeproject.org/exposure/listing/full-list"
CACHE = cache = SQLiteBackend(cache_name="cache", include_headers=True)


async def importProjects(startAt=0, endAt=-1, getWorkspaces=True, getMetadata=True, overwrite=False):
    """
    Imports all the projects in the database
    """

    projectExposureLinks = await getProjectsList(startAt, endAt)
    with open("Allprojects.json", "w") as f:
        json.dump(projectExposureLinks, f)

    numProjects = len(projectExposureLinks)
    logger.info("Importing {} projects".format(numProjects))

    project_urls_task = []
    async with CachedSession(cache=CACHE) as session:
        for project in projectExposureLinks:
            logger.debug(f'Getting Links for {project}')
            projectName = project.split('/')[-1]
            os.makedirs(f'projects/{projectName}', exist_ok=True)
            project_urls_task.append(getProjectHrefs(session, project))

        projectLinks = await asyncio.gather(*project_urls_task, return_exceptions=False)
        with open('projectLinks.json', 'w') as f:
            json.dump(projectLinks, f, indent=4)
        # Extract the metadata we can from each project
        metadata_tasks = []
        metadata = []

        for projectlink in projectLinks:

            projectName = projectlink['project'].split('/')[-1]
            if(getMetadata):
                metadata_tasks.append(asyncio.ensure_future(getProjectInfo(session,
                                                                           projectlink)))

        metadata = await asyncio.gather(*metadata_tasks, return_exceptions=False)
        with open('projects.json', 'w') as f:
            json.dump(metadata, f, indent=4)

    # have to do this synchronously because otherwise we seem to be overloading the pmr git server
    if(getWorkspaces):
        sleep(2)
        getGitRepos(projectLinks)


def getProjectHash(id):
    """
    Returns the hash of the project
    """
    with open("projects.json", "r") as f:
        projects = json.load(f)
        for project in projects:
            if(project['identifier'] == id):
                return project['hash']


async def getProjectsList(startAt=0, endAt=-1):
    """
    Returns a list of all the projects in the database
    """

    async with CachedSession(cache=CACHE) as session:
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
        logger.success(f'Got links for {projectExposureHref}')

        exposure_links = exposure_info['collection']['links']
        # Handle this weirdness for  PMR2/pmr2.app#6
        if(projectExposureHref == "https://models.physiomeproject.org/exposure/e340f005288ec6bd49535cf792769dd0"):
            exposure_links = []
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
                        print("Failure to get file info for: ",
                              projectExposureHref)
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
                        else:
                            created_file_links['title'] = file_prompt
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
        sleep(1)
        projectName = projectLink['project'].split('/')[-1]
        success.append(getGitRepo(projectName, projectLink['workspace']))

    # Delete all the .git folders and .gitmodules files to prevent issues with top level git repo
    logger.debug(f'Deleting .git folders and .gitmodules files')
    os.system('find ./projects -type d -name ".git" -ls -exec rm -rvf {} +')
    os.system('find ./projects -type f -name ".git" -ls -exec rm -rvf {} +')
    os.system('find ./projects -type f -name ".gitmodules" -delete')


def getGitRepo(name, link):
    logger.debug(f'Getting git repo for {name}')
    shutil.rmtree(f'projects/{name}/workspace', ignore_errors=True)
    project_hash = getProjectHash(name)
    if(link):
        try:
            logger.info(f'Cloning {name}')
            os.system(
                f'git clone --recurse-submodules {link} projects/{name}/workspace ')
            if(project_hash):
                cwd = os.getcwd()
                os.chdir(f'projects/{name}/workspace')
                os.system(f'git checkout {project_hash}')
                os.chdir(cwd)
            shutil.rmtree(
                f'projects/{name}/workspace/.git', ignore_errors=True)
            shutil.rmtree(
                f'projects/{name}/workspace/.gitmodules', ignore_errors=True)
        except Exception as e:
            logger.error(e)
            return False

    return True


def parseHTMLPage(html_page, model_metadata):

    soup = BeautifulSoup(html_page, 'html.parser')
    if(not soup):
        logger.error(f'Failed to parse HTML for {html_page}')

        raise Exception(f'Failed to parse HTML for {html_page}')
    content = soup.find('div', id='content')
    if(not content):
        logger.error(f'Failed to parse HTML Content for {html_page}')
        raise Exception(f'Failed to parse HTML Content for {html_page}')

    title = content.find('h1').text.strip()
    summary = content.find(
        'div', id='parent-fieldname-description')
    if(summary):
        summary = summary.text.strip()
    else:
        summary = None

    model_metadata['summary'] = summary
    
    images = soup.find_all(
        "img", class_="tmp-doc-informalfigure")

    for image in (images or []):

        model_metadata['thumbnails'].append(image['src'])


    content_core = content.find('div', id='content-core')
    children = content_core.findChildren(recursive=True)
    for child in (children or []):
        
        if child.name == 'title':
            child.decompose()
        elif child.name == 'table':
            child.decompose()
        else:
            pass
    description = markdownify.markdownify(str(content_core).strip())
    
    with open(f'descriptions', 'a') as f:
        f.write(description)
  

    # We might have the title already from the JSON call above
    if(title and model_metadata['title'] == ''):
        model_metadata['title'] = title

    model_metadata['description'] = description

    return model_metadata


def parseMetadata(req, model_metadata):
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
    return model_metadata


async def getProjectInfo(session, projectlink):
    """

    """
    project_href = projectlink['project']
    workspace_href = projectlink['workspace']

    projectName = project_href.split('/')[-1]
    project_content = projectlink['content']

    model_metadata = {
        "identifier": "",
        "hash": "",
        "title": None,
        "description": None,
        "summary": None,
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
        "content_metadata": [],
        "contributor": "Bilal Shaikh",
        "errors": [],
    }
    # This is the main page that is displayed for each model

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
        async with session.get(project_href, headers={'Accept': 'text/html'}) as resp:
            logger.debug(f'Getting documentation for {projectName}')
            try:
                html_page = (await resp.text())

                if(html_page):
                    model_metadata = parseHTMLPage(html_page, model_metadata)

            except Exception as e:
                logger.error(
                    f'Failed to get documentation for {projectName}, {repr(e)}')
                # logger.error({html_page})

                model_metadata['errors'].append(repr(e))
    else:
        logger.error(
            f'Failed to get project info for {projectName} due to missing project href')
        model_metadata['errors'].append('No project href')

    # The metadata may be present in the first child of the content. We can use it for the whole project,otherwise the top level projects won't have it
    if(len(project_content) > 0):
        metadata_href = project_content[0].get('metadata')
    else:
        metadata_href = None

    if(metadata_href):
        async with session.get(metadata_href, headers={'Accept': 'application/json'}) as resp:
            logger.debug(f'Getting metadata for {projectName}')
            try:
                req = await resp.json()
                model_metadata = parseMetadata(req, model_metadata)
            except(Exception) as e:
                logger.error(
                    f'Failed to get metadata for {projectName}, {repr(e)}')
                model_metadata['errors'].append(repr(e))

    else:
        logger.error(
            f'Failed to get metadata for {projectName} due to missing metadata href')
        model_metadata['errors'].append('No metadata href')

    # Now do the same parsing for all the children of the project
    for child in project_content:
        metadata_href, documentation_href, href = child["metadata"], child["documentation"], child["href"]
        title = child["title"]
        file_name = child["file_name"]
        child_metadata = {
            "title": child["title"],
            "file_name": child["file_name"],
            "file_type": child["file_type"],
            "tags": [],
            "citation": {
                "title": None,
                "authors": None,
                "journal": None,
                "identifier": None,
            },
            "authors": None,
            "description": None,
            "summary": None,
            "thumbnails": [],
            "errors": [],
        }

        if(metadata_href):
            async with session.get(metadata_href, headers={'Accept': 'application/json'}) as resp:
                logger.debug(f'Getting metadata for {projectName}/{file_name}')
                try:
                    req = await resp.json()
                    metadatas = req['collection']['items'][0]['data']
                    for metadata in metadatas:
                        if metadata['name'] == 'keywords':
                            child_metadata['tags'] = metadata['value']
                        if metadata['name'] == 'citation_title':
                            child_metadata['citation']['title'] = metadata['value']
                        if metadata['name'] == 'citation_authors':
                            child_metadata['citation']["authors"] = metadata['value']
                        if metadata['name'] == 'citation_journal':
                            child_metadata['citation']['journal'] = metadata['value']
                        if metadata['name'] == 'citation_id':
                            child_metadata['citation']['identifier'] = metadata['value']
                        if metadata['name'] == 'model_author':
                            child_metadata['authors'] = metadata['value']
                except(Exception) as e:
                    logger.error(
                        f'Failed to get metadata for {file_name}, {repr(e)}')
                    child_metadata['errors'].append(repr(e))

        if(documentation_href):
            async with session.get(documentation_href, headers={'Accept': 'text/html'}) as resp:
                logger.debug(
                    f'Getting documentation for {projectName}/{file_name}')
                try:
                    html_page = (await resp.text())

                    if(html_page):
                        child_metadata = parseHTMLPage(
                            html_page, child_metadata)
                except Exception as e:
                    logger.error(
                        f'Failed to get documentation for {file_name}, {repr(e)}')
                    child_metadata['errors'].append(repr(e))
        model_metadata['content_metadata'].append(child_metadata)

    return model_metadata
