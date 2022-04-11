
from re import S
from . import load_projects, process_projects, submit_projects
import asyncio
import fire
import json
from loguru import logger
CONFIG = {
    "GetWorkspaces": False,
    "GetMetadata": True,
    "GetArchives": False,
    "Overwrite": True,
    "LogLevel": "WARNING",
    "LogFile": "log.txt",
    "ClearProjects": False,
    "StartAt": 0,
    "EndAt": -1
}


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

    def process(self, project_id=None, projects_file="projects.json", projects_dir="projects"):

        logger.debug(f'Processing projects from {projects_file}')
        projects = json.load(open(projects_file))
        skips = json.load(open("skip.json"))
        all_skipped_projects = []
        for skip in skips:
            skipped_projects = skip["projects"]
            all_skipped_projects.extend(skipped_projects)

        projects = [project for project in projects if project["identifier"]
                    not in all_skipped_projects]

        def process_sub(project):
            projects_info = []
            logger.debug(f'Processing project {project["title"]}')
            project_dir = f'{projects_dir}/{project["identifier"]}'
            project_info = process_projects.process(project, project_dir)
            projects_info.append(project_info)
            return projects_info

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
            for project in projects:
                if not project["title"]:
                    continue
                project_info = process_sub(project)
                projects_info.append(project_info[0])

            # write projects_info as json to file
            with open('projects.processed.json', 'w') as outfile:
                json.dump(projects_info, outfile, indent=4)

    def submit(self, project_id=None, projects_file="projects.json", out_dir="output"):
        logger.debug(f'Submitting projects from {projects_file}')
        submit_projects.submit()


def main():
    fire.Fire(BiosimulationsPhysiome)
