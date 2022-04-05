from ensurepip import version
import json
from time import sleep
from biosimulators_utils.biosimulations import utils
from loguru import logger
import requests


def submit():
    projects = json.load(open("projects.processed.json"))
    #projects = [project for project in projects if project["has_sedml"]]

    OUT_DIR = "out"
    runs = []
    for project in projects:
        
        run_id = utils.run_simulation_project(
            project['identifier'],
            f'{OUT_DIR}/{project["identifier"]}/{project["identifier"]}.omex',
            "opencor",

            simulator_version="latest",

            purpose="academic",

        )
        logger.debug(f'Submitting project {project["title"]}')
        logger.success(
            f'Submitted project https://run.biosimulations.org/runs/{run_id}')
        runs.append(
            {"runId": run_id,"id": project["identifier"], "url": f'https://run.biosimulations.org/runs/{run_id}', "status": 'submitted'})

    completed = False

    while(not completed):
        for run in runs:

            api_run = requests.get(
                f'https://api.biosimulations.org/runs/{run["runId"]}')
            api_run.raise_for_status()
            run['status'] = api_run.json()['status']
            logger.debug(f'{run["id"]} {run["status"]}')

        completed = all(
            [(run['status'] == 'SUCCEEDED' or run['status'] == 'FAILED') for run in runs])
        logger.warning([run['status'] for run in runs])
        logger.info("Check again")
        logger.info(completed)
        sleep(20)
        json.dump(runs, open('runs.json', 'w'), indent=4)
    json.dump(runs, open('runs.json', 'w'), indent=4)


if __name__ == "__main__":
    submit()
