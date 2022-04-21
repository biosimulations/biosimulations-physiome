from sympy import O
from . import load_projects, process_projects, submit_projects, run_projects
import asyncio
import fire
import json
from loguru import logger
from joblib import Parallel, delayed
CONFIG = {
    "GetWorkspaces": True,
    "GetMetadata": True,
    "GetArchives": False,
    "Overwrite": True,
    "LogLevel": "WARNING",
    "LogFile": "log.txt",
    "ClearProjects": False,
    "StartAt": 0,
    "EndAt": -1
}


def get_non_skipped_projects(projects_file):
    with open(projects_file, 'r') as f:
        projects = json.load(f)
        #projects = [project for project in projects if project["has_sedml"]]
        try:
            skips = json.load(open("skip.json"))
        except FileNotFoundError:
            skips = []
        all_skipped_projects = []
        for skip in skips:
            skipped_projects = skip["projects"] if skip["skip"] else []
            all_skipped_projects.extend(skipped_projects)
        projects = [project for project in projects if project["identifier"]
                    not in all_skipped_projects]
        projects=[projects for projects in projects if projects["title"]]
        return projects


class BiosimulationsPhysiome:

    def __init__(self, config_file=None):
        logger.info("BiosimulationsPhysiome")
        logger.level(CONFIG["LogLevel"])
        if config_file:
            self.config = json.load(open(config_file))
        else:
            self.config = CONFIG

    def load(self):

        config = self.config

        logger.debug("Loading projects from Physiome Repository")

        asyncio.run(load_projects.importProjects(startAt=config['StartAt'],
                                                 endAt=config['EndAt'], getMetadata=config['GetMetadata'],
                                                 getWorkspaces=config['GetWorkspaces'], overwrite=config['Overwrite'],))

    def process(self, project_id=None, projects_file="projects.json", projects_dir="projects", projects_ouput_file="cache/projects.processed.json"):

        projects = get_non_skipped_projects(projects_file)

        def process_sub(project):
            logger.debug(f'Processing project {project["title"]}')
            project_dir = f'{projects_dir}/{project["identifier"]}'
            project_info = process_projects.process(project, project_dir)
            return project_info

        if project_id:
            project = [
                project for project in projects if project["identifier"] == str(project_id)][0]

            logger.debug(project)
            project_info = process_sub(project)
            path = f'{project["identifier"]}.proccessed.json'
            with open(path, 'w') as outfile:
                json.dump(project_info, outfile, indent=4)

        else:
            
            projects_info = []
            projects_info = Parallel(n_jobs=12)(delayed(process_sub)(project) for project in projects)
            # for project in projects:
            #     project_info = process_sub(project)
            #     projects_info.append(project_info[0])

            # write projects_info as json to file
            with open(projects_ouput_file, 'w') as outfile:
                json.dump(projects_info, outfile, indent=4)
    def run (self, project_id=None, projects_file="projects.processed.json"):
        projects = get_non_skipped_projects(projects_file)
        successes, failures =run_projects.run_projects(projects)
        json.dump(successes, open('projects_to_submit.json', 'w'), indent=4)
        
        
       
    def submit(self, project_id=None, projects_file="projects_to_submit.json", out_dir="output"):
        logger.debug(f'Submitting projects from {projects_file}')
        projects = get_non_skipped_projects(projects_file)
        submit_projects.submit(projects)


def main():
    fire.Fire(BiosimulationsPhysiome)
