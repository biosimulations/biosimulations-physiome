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
from constants import NO_LOG_FILE
from tqdm import tqdm
client = docker.from_env()

TIMEOUT_LIMIT = 60*10

MAX_RUNNING_CONTAINERS = 20
NAME_PREFIX = 'physiome-opencor-'
NO_LOG_FILE = "NOLOGREADFROMOUTPUT"


def check_failures():
    failed_runs = json.load(open('failures.json'))
    logger.info("Loading logs for failed runs")
    logs = [yaml.safe_load(open(f'runs/{run}/log.yml')) if os.path.exists(
        f'runs/{run}/log.yml') else None for run in tqdm(failed_runs)]
    logger.info("Checking for missing logs")
    failed = [(run, log) for run, log in zip(failed_runs, logs)]
    failed_runs_with_logs = [ (run, log.get("exception", {"message": NO_LOG_FILE})) if log is not None else (run, {"message": NO_LOG_FILE}) for run, log in failed ]
    failed_runs_with_logs  = [(run, log) if log else (run, {'message': NO_LOG_FILE}) for run, log in failed_runs_with_logs ]
    
    
  
    json.dump(failed_runs_with_logs, open(
        'failed_runs_with_logs.json', 'w'), indent=4)
    error_types = {}
    error_indicators = {
        NO_LOG_FILE: "SimulationDidNotStartError",
        "mxstep steps taken before reaching tout": "MaxIterationsError",
        "encountered unsupported operator partialdiff": "UnsupportedPdeError",
        "Error: the model is underconstrained (i.e. some variables need to be initialised or computed)": "UnderConstrainedError",
        "has in interfaces, but is not connected (directly or indirectly) to any variable with no in interfaces": "DisconnectedInterfaceError",
        "Error: the model is unsuitably constrained (i.e. some variables could not be found and/or some equations could not be used)": "UnconstrainedError",
        "the corrector convergence test failed repeatedly": "ConvergenceError",
        "The target of each variable must be a valid observable.": "InvalidObservableError",
        "does not contain any executing SED-ML files": "NoSedmlError",
        "the system function failed at the first call": "UncategorizedRuntimeError",
        "encountered unsupported operator sum;": "InvalidCellMLError",
        "The SED-ML file at location": "InvalidSedmlError",
        "An OMEX XML document must conform to the XML Schema for the corresponding OMEX Level": "InvalidManifestError",
        "Plot must have at least one curve": "InvalidPlotError",
        "the error test failed repeatedly": "ConvergenceError",
        "variable has units": "UnitsError",
        "invalid units": "UnitsError",
        "the model must have at least one ODE or DAE": "NoEquationsError",
        "cannot find variable ": "VariableNotFoundError",

    }
    logger.info("Categorizing errors")
    for run, error in tqdm(failed_runs_with_logs):
        logger.debug(f'Checking {run}')
        if not error:
            logger.exception("No error found")
        error_message = error.get("message", "")
        for indicator, error_type in error_indicators.items():
            if error_message.find(indicator) != -1:
                somelist = error_types.get(error_type, [])
                somelist.append(run)
                error_types[error_type] = somelist
                break
        else:
            somelist = error_types.get(
                "UncategorizedError", [])
            somelist.append((run, error_message))
            error_types["UncategorizedError"] = somelist

    json.dump(error_types, open('error_types.json', 'w'), indent=4)


if __name__ == "__main__":
    # run_projects()
    check_failures()
