from asyncio.log import logger
from curses import meta
from distutils.command.build import build
import logging
import shutil
import time
from dataclasses import dataclass, asdict

import biosimulators_utils
import Bio
from biosimulators_utils.combine.data_model import CombineArchive, CombineArchiveContent, CombineArchiveContentFormat
from biosimulators_utils.combine.io import CombineArchiveWriter
from biosimulators_utils.config import Config
from biosimulators_utils.omex_meta.data_model import BIOSIMULATIONS_ROOT_URI_FORMAT, OmexMetadataOutputFormat
from biosimulators_utils.omex_meta.io import BiosimulationsOmexMetaWriter, BiosimulationsOmexMetaReader
from biosimulators_utils.omex_meta.utils import build_omex_meta_file_for_model
from biosimulators_utils.ref.data_model import Reference, JournalArticle, PubMedCentralOpenAccesGraphic  # noqa: F401
from biosimulators_utils.ref.utils import get_reference, get_pubmed_central_open_access_graphics
from biosimulators_utils.sedml.data_model import (
    SedDocument, Model, ModelLanguage, SteadyStateSimulation,
    Task, DataGenerator, Report, DataSet)
from biosimulators_utils.sedml.io import SedmlSimulationWriter
from biosimulators_utils.sedml.model_utils import get_parameters_variables_outputs_for_simulation
from biosimulators_utils.viz.vega.escher import escher_to_vega
from biosimulators_utils.warnings import BioSimulatorsWarning
import os 
import json

OUT_DIR = "out"

Bio.Entrez.email = os.getenv('ENTREZ_EMAIL', None)
ENTREZ_DELAY = 0.5


def clean_output_dir(project_out_dir):
    if os.path.exists(project_out_dir):
        # We want to remove the errors and metadata files
        #keep the journal info to prevent api calls
        shutil.rmtree(project_out_dir+"/errors.txt", ignore_errors=True)
        shutil.rmtree(project_out_dir+"/metadata.rdf", ignore_errors=True)

def process(metadata, project_path):
    logger = logging.getLogger(__name__)
    project_out_dir = os.path.join(OUT_DIR, metadata["identifier"])
    clean_output_dir(project_out_dir)
    os.makedirs(project_out_dir, exist_ok=True)
    journal_article = None
    journal_article_authors = []
    if(metadata['citation']['identifier']):
        journal_path = project_out_dir + "/journal.json"
        if(os.path.isfile(journal_path)):
            print(journal_path)
            journal_article = json.load(open(journal_path))
            print(journal_article)            
            journal_article = JournalArticle(**journal_article)
            print(journal_article)
            journal_article_authors = journal_article.authors
            

        else:
            pmid= metadata['citation']['identifier']
            
            # Handle case of https://models.physiomeproject.org/exposure/9d48e39f893b5f1e98e53778f606c2c2/bhalla_iyengar_1999_j.cellml/view
            if(pmid=="urn:miriam:pubmed:99105994"):
                pmid="urn:miriam:pubmed:9888852"
            if(pmid=="urn:miriam:pubmed:10545344"):
                pmid="urn:miriam:pubmed:20540926"
            pmid= pmid.split(":")[-1]
            print("pmid:",pmid)
            print()

            time.sleep(ENTREZ_DELAY)
            # Temporary handle case when pmid is 11368770 due to wierdness in enterez DOI
            if(pmid!="None" and pmid!="" and pmid!= "11368770" and pmid!="8713663"):
                journal_article = get_reference(pmid)
                journal_article_authors = journal_article.authors
                with open(project_out_dir+"/journal.json", "w") as f:
                    json.dump(asdict(journal_article), f)
            else:
                journal_article = None
                journal_article_authors = []


    # Todo default contributor to file/config 
    contributors =   [{
                "label": "Bilal Shaikh",
                "uri": 'http://identifiers.org/orcid:0000-0001-5801-5510'
  
            } ]
    model_author = metadata['authors']
    if(model_author):
        contributors.append({
                "label": model_author,
                "uri": None
        })
    
        
    creators= []
    for author in journal_article_authors:
        creators.append({
            "label": author,
            "uri": None
        })

    
    
    
    


    contents_path = project_path +"/omexContents"
    contents= os.listdir(contents_path)
    model_file= None
    sedml_file = None
        
    for content in contents:
        if(content.endswith(".sedml")):
            sedml_file = content
        if(content.endswith(".cellml")):
            model_file = content
    

    omex_metadata=[{
        'uri': '.',
        "combine_archive_uri": BIOSIMULATIONS_ROOT_URI_FORMAT.format(metadata["identifier"]),
        "title": metadata["title"],
        "abstract": None,
        "keywords": [tag[-1] for tag in (metadata["tags"] or []) if tag is not None and len(tag) > 1],
        "description": metadata["description"],
        "license": {
            "uri": "https://creativecommons.org/licenses/by/3.0/",
            "label": "CC BY 3.0",
        },
        "contributors": [],
        "creators": creators,
        'identifiers': [{
             "label": "PMR",
             # TODO: URL appropriate namespace 'e' or 'exposure'
             "uri": "https://identifiers.org/pmr:{}/{}".format('e', metadata["identifier"])
         }],
        'predecessors': [],
        'successors': [],
        'see_also': [],
        'funders': [],
        'other':[],


    }]   
    write_metadata(omex_metadata, project_out_dir)


def write_metadata(metadata, project_out_dir):
    

    config = Config(OMEX_METADATA_OUTPUT_FORMAT=OmexMetadataOutputFormat.rdfxml)
    BiosimulationsOmexMetaWriter().run(metadata, project_out_dir+"/metadata.rdf", config=config)
    _, errors, warnings = BiosimulationsOmexMetaReader().run(project_out_dir+"/metadata.rdf")
    print(errors)
    if(errors):
        with open(project_out_dir+"/errors.txt", "w") as f:
            f.write(str(errors))

    
