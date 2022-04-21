from ensurepip import version
import json
from time import sleep
from biosimulators_utils.biosimulations import utils
from loguru import logger
from .auth import get_token
import requests


def submit(projects):
    logger.debug(projects)
    OUT_DIR = "out"
    runs = []
    token = get_token()
    for index, project in enumerate(projects):

        run_id = utils.run_simulation_project(
            project['identifier'],
            f'{OUT_DIR}/{project["identifier"]}/{project["identifier"]}.omex',
            "opencor",
            simulator_version="latest",
            purpose="academic",
            auth=token,
            project_id=project['title'],
        )
        if(not index == 0 and index % 20 == 0):
            check_runs(runs)
            sleep(60)
        logger.debug(f'Submitting project {project["title"]}')
        logger.success(
            f'Submitted project https://run.biosimulations.org/runs/{run_id}')
        runs.append(
            {"runId": run_id, "id": project["identifier"], "url": f'https://run.biosimulations.org/runs/{run_id}', "status": 'submitted'})

    completed = False

    while(not completed):
        completed = check_runs(runs)
        sleep(20)


def check_runs(runs):
    runs_to_check = [run for run in runs if not(
        (run['status'] == 'SUCCEEDED' or run['status'] == 'FAILED'))]
    for run in runs_to_check:

        api_run = requests.get(
            f'https://api.biosimulations.org/runs/{run["runId"]}')
        api_run.raise_for_status()
        run['status'] = api_run.json()['status']
        logger.debug(f'{run["id"]} {run["status"]}')

    completed = all(
        [(run['status'] == 'SUCCEEDED' or run['status'] == 'FAILED') for run in runs])

    failed_runs = [run for run in runs if run['status'] == 'FAILED']
    success_runs = [run['id'] for run in runs if run['status'] == 'SUCCEEDED']
    json.dump(success_runs, open('success_runs.json', 'w'))
    json.dump(failed_runs, open('failed_runs.json', 'w'))
    json.dump(runs, open('runs.json', 'w'), indent=4)
    return completed


if __name__ == "__main__":
    submit()
