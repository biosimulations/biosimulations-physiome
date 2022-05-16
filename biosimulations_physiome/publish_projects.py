import requests
import json
from loguru import logger
import string
from .auth import get_token


def publish(projects):
    projects_to_publish = json.load(open("projects_to_submit.json"))
    for project in projects:
        # find the project in the list of projects to publish
        project_to_publish = [
            p for p in projects_to_publish if p['identifier'] == project['id']][0]

        project_id = project["id"]
        runId = project["runId"]
        title = project_to_publish["title"]
        project_title = title.replace(", ", "-")
        project_title = project_title.replace(",", "-")
        project_title = project_title.replace(" ", "-")
        project_title = project_title.replace(".", "-")
        project_title = project_title.replace("/", "-")
        project_title = project_title.replace("(", "_")
        project_title = project_title.replace(")", "_")
        project_title = project_title.replace(":", "-")
        project_title = project_title.replace("+", "")
        project_title = project_title.replace("[", "")
        project_title = project_title.replace("]", "")
        project_title = project_title.replace("'", "")
        project_title = project_title.translate(
            str.maketrans('', '', string.whitespace))
        project_title = project_title.strip()

        print(title)
        print(project_title)

        res = requests.get(
            f'https://api.biosimulations.org/runs/{project["runId"]}/validate')

        status_code = res.status_code
        if status_code != 204:
            logger.error(f'{project_id} {title} failed validation')

        else:
            token = get_token()

            if status_code == 204:
                res = requests.post(
                    f'https://api.biosimulations.org/projects/{project_title}/', data={
                        "id": project_title,
                        "simulationRun": runId
                    },
                    headers={
                        "Authorization": token,
                    }

                )

                project_status = res.status_code
                if project_status == 400:
                    logger.error(
                        f'Project {project_title} failed {res.json()}')
                if project_status == 409:
                    logger.warning(f'Project {title} already exists')
                elif project_status == 201:
                    logger.success(f'Project {title} created')
