from ast import arguments
import shutil
from time import sleep
import time
from unicodedata import name
from requests import request
import requests
import json
import docker
from docker.errors import ContainerError
import os
from loguru import logger
import yaml
from .constants import NAME_PREFIX, MAX_RUNNING_CONTAINERS, TIMEOUT_LIMIT
client = docker.from_env()


def filter_containers(containers):
    return [container for container in containers if container.name.startswith(NAME_PREFIX)]


def get_paused_containers():
    all_containers = client.containers.list(
        all=True, filters={'status': 'paused'})
    return filter_containers(all_containers)


def get_running_containers():
    return filter_containers(client.containers.list(all=True, filters={'status': 'running'}))


def get_exited_containers():
    return filter_containers(client.containers.list(all=True, filters={'status': 'exited'}))


def get_container_name(project_id):
    return f'{NAME_PREFIX}{project_id}'


def get_container_project_id(container):
    return container.name.split('-')[-1]


def run_projects(projects):
    

    input_path_prefix = os.path.abspath('out/')
    output_path_prefix = os.path.abspath('runs/')
    successes = []
    failures = []
    containers = []

    for container in get_paused_containers():
        container.kill()
        container.remove()
    for container in get_exited_containers():
        container.remove()

    for container in get_running_containers():
        container.kill()
        container.remove()

    logger.debug("Removed old containers")
    start_time = time.time()
    for project in projects:
        project_id = project['identifier']

        shutil.rmtree(f'{output_path_prefix}/{project_id}', ignore_errors=True)

        container = client.containers.run('ghcr.io/biosimulators/opencor:latest',  volumes=[
            f'{input_path_prefix}:/in', f'{output_path_prefix}:/out'], command=f' --archive /in/{project_id}/{project_id}.omex -o /out/{project_id}/', detach=True, name=f'{get_container_name(project_id)}')
        container.pause()
        containers.append(container)
    total_containers = len(containers)
    successes = []
    failures = []
    pending = []
    running_count = 0
    paused_containers = get_paused_containers()
    running_containers = get_running_containers()
    finished_containers = get_exited_containers()
    while(len(paused_containers) + len(running_containers) > 0):

        logger.info(f'{len(paused_containers)} paused containers')
        logger.info(f'{len(running_containers)} running containers')
        logger.info(f'{len(finished_containers)} finished containers')
        logger.success(f'{len(successes)} successes')
        logger.error(f'{len(failures)} failures')

        for container in finished_containers:
            result = container.wait()
            status_code = result['StatusCode']
            if(status_code == 0):
                successes.append(get_container_project_id(container))
                container.remove()
            else:
                failures.append(get_container_project_id(container))
                container.remove()
        started = 0
        for container in paused_containers:
            if(len(running_containers) + started < MAX_RUNNING_CONTAINERS):
                container.unpause()
                started += 1

        paused_containers = get_paused_containers()
        running_containers = get_running_containers()
        finished_containers = get_exited_containers()

        json.dump(successes, open('successes.json', 'w'), indent=4)
        json.dump(failures, open('failures.json', 'w'), indent=4)

        current_time = time.time()
        if(current_time - start_time > TIMEOUT_LIMIT):
            logger.error(f'Timeout limit reached')
                        
            for container in get_running_containers():
                logger.error("Killing container" + container.name)
                container.kill()
                failures.append(container.name)
                container.remove()
            for container in get_paused_containers():
                logger.error("Killing container" + container.name)
                container.unpause()
                container.kill()
                failures.append(container.name)
                container.remove()
            

        sleep(2)

    logger.success(f'{len(successes)} successes')
    logger.success(successes)
    logger.error(f'{len(failures)} failures')
    logger.error(failures)
    json.dump(successes, open('successes.json', 'w'), indent=4)
    json.dump(failures, open('failures.json', 'w'), indent=4)
    success_projects = [project for project in projects if project['identifier'] in successes]
    failure_projects = [project for project in projects if project['identifier'] in failures]
    
    return success_projects, failure_projects


if __name__ == "__main__":
    projects = json.load(open('projects.processed.json'))
    run_projects(projects)
