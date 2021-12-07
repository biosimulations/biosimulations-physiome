from .load_projects import importProjects
import asyncio
import fire
import json
class BiosimulationsPhysiome:
    def __init__(self,):
        print("BiosimulationsPhysiome")

    def load(self):      
        print("Loading projects from Physiome Repository")
        asyncio.run(importProjects())

    def process(self, projects_file="projects.json", projects_dir="projects"):
        print(f'Processing projects from {projects_file}')
        projects = json.load(open(projects_file))
        print(projects)
        for project in projects:
            print(f'Processing project {project["name"]}')
        
        


def main():
    fire.Fire(BiosimulationsPhysiome)

