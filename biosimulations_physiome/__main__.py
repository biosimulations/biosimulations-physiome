
from . import load_projects, process_projects
import asyncio
import fire
import json
import logging
from .logging import setup_logging
CONFIG = {
    "GetWorkspaces": True,
    "GetMetadata": True,
    "GetArchives": True,
    "LogLevel": "DEBUG",
    "LogFile": "log.txt",
    "ClearProjects": False,
    "StartAt": 0,
    "EndAt": -1
}


class BiosimulationsPhysiome:

    def __init__(self, config_file=None):
        log_level = logging.DEBUG
        logging.getLevelName(CONFIG["LogLevel"])
        log_file = CONFIG["LogFile"]
        log_file_level = logging.DEBUG

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_file_level)
        # create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        self.config = CONFIG
        print("BiosimulationsPhysiome")
        if config_file:
            self.config = json.load(open(config_file))

    def load(self):

        config = self.config

        print("Loading projects from Physiome Repository")
        asyncio.run(load_projects.importProjects(clearProjects=config['ClearProjects'], startAt=config['StartAt'],
                                                 endAt=config['EndAt'], getArchives=config['GetArchives'], getMetadata=config['GetMetadata'],
                                                 getWorkspaces=config['GetWorkspaces']))

    def process(self, project_id=None, projects_file="projects.json", projects_dir="projects"):

        print(f'Processing projects from {projects_file}')
        projects = json.load(open(projects_file))

        def process_sub(project):
            projects_info = []
            print(f'Processing project {project["title"]}')
            project_dir = f'{projects_dir}/{project["identifier"]}'
            project_info = process_projects.process(project, project_dir)
            projects_info.append(project_info)
            return projects_info

        if project_id:
            project = [
                project for project in projects if project["identifier"] == project_id][0]

            print(project)
            project_info = process_sub(project)
            path = f'{project["identifier"]}.proccessed.json'
            with open(path, 'w') as outfile:
                json.dump(project_info, outfile, indent=4)

        else:
            for project in projects:
                if not project["title"]:
                    continue
                projects_info = process_sub(project)

            # write projects_info as json to file
            with open('projects.processed.json', 'w') as outfile:
                json.dump(projects_info, outfile, indent=4)


def main():
    fire.Fire(BiosimulationsPhysiome)
