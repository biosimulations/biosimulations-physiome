from ensurepip import version
import json
from time import sleep
from biosimulators_utils.biosimulations import utils
from loguru import logger
import requests


def submit():
    projects = json.load(open("projects.processed.json"))
    #projects = [project for project in projects if project["has_sedml"]]
    skips = json.load(open("skip.json"))
    all_skipped_projects = []
    for skip in skips:
        skipped_projects = skip["projects"]
        all_skipped_projects.extend(skipped_projects)
    projects = [project for project in projects if project["identifier"]
                not in all_skipped_projects]
    OUT_DIR = "out"
    runs = []
    for index, project in enumerate(projects):

        run_id = utils.run_simulation_project(
            project['identifier'],
            f'{OUT_DIR}/{project["identifier"]}/{project["identifier"]}.omex',
            "opencor",

            simulator_version="latest",

            purpose="academic",

        )
        if(not index == 0 and index % 20 == 0):
            check_runs(runs)
            sleep(30)
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
    for run in runs:

        api_run = requests.get(
            f'https://api.biosimulations.org/runs/{run["runId"]}')
        api_run.raise_for_status()
        run['status'] = api_run.json()['status']
        logger.debug(f'{run["id"]} {run["status"]}')

    completed = all(
        [(run['status'] == 'SUCCEEDED' or run['status'] == 'FAILED') for run in runs])

    json.dump(runs, open('runs.json', 'w'), indent=4)
    return completed


if __name__ == "__main__":
    submit()
