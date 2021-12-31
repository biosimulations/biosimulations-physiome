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
from biosimulators_utils.ref.data_model import Reference, JournalArticle
from biosimulators_utils.ref.utils import get_reference
from biosimulators_utils.sedml.data_model import (
    SedDocument, Model, ModelLanguage, SteadyStateSimulation,
    Task, DataGenerator, Report, DataSet)
from biosimulators_utils.sedml.io import SedmlSimulationWriter
from biosimulators_utils.sedml.model_utils import get_parameters_variables_outputs_for_simulation

from biosimulators_utils.warnings import BioSimulatorsWarning
import os
import json


OUT_DIR = "out"

Bio.Entrez.email = os.getenv('ENTREZ_EMAIL', None)
ENTREZ_DELAY = 0.5


combine_writer = CombineArchiveWriter()


def get_content_format_from_file_extension(file_extension):

    file_endings_to_format = {
        "cellml": CombineArchiveContentFormat.CellML,
        "png": CombineArchiveContentFormat.PNG,
        "PNG": CombineArchiveContentFormat.PNG,
        "svg": CombineArchiveContentFormat.SVG,
        "jpg": CombineArchiveContentFormat.JPEG,
        "jpeg": CombineArchiveContentFormat.JPEG,
        "omex": CombineArchiveContentFormat.OMEX,
        "sedml": CombineArchiveContentFormat.SED_ML,
        "sed-ml": CombineArchiveContentFormat.SED_ML,
        "bmp": CombineArchiveContentFormat.BMP,
        "xml": CombineArchiveContentFormat.XML,
        "rdf": CombineArchiveContentFormat.XML,
        "json": CombineArchiveContentFormat.JSON,
        "gif": CombineArchiveContentFormat.GIF,
        "pdf": CombineArchiveContentFormat.PDF,
        "m": CombineArchiveContentFormat.MATLAB,
        "rst": CombineArchiveContentFormat.TEXT,
        "py": CombineArchiveContentFormat.Python,
        "ipynb": CombineArchiveContentFormat.IPython_Notebook,
        "zip": CombineArchiveContentFormat.ZIP,
        "csv": CombineArchiveContentFormat.CSV,
        "sbgn": CombineArchiveContentFormat.SBGN,
        "txt": CombineArchiveContentFormat.TEXT,
        "md": CombineArchiveContentFormat.TEXT,
        "xlsx": CombineArchiveContentFormat.XLSX,
        "h5": CombineArchiveContentFormat.HDF5,

        # TODO add the formats to biosimulators_utils ( see)

        "dll": CombineArchiveContentFormat.OTHER,
        "so": CombineArchiveContentFormat.OTHER,
        "conf": CombineArchiveContentFormat.OTHER,
        "rb": CombineArchiveContentFormat.OTHER,
        "svgz": CombineArchiveContentFormat.SVG,
        "docx": CombineArchiveContentFormat.OTHER,
        "rtf": CombineArchiveContentFormat.TEXT,
        "RTF": CombineArchiveContentFormat.TEXT,
        "pptx": CombineArchiveContentFormat.OTHER,
        "xls": CombineArchiveContentFormat.XLSX,
        "eps": CombineArchiveContentFormat.OTHER,
        "js": CombineArchiveContentFormat.OTHER,
        "ai": CombineArchiveContentFormat.OTHER,
        "html": CombineArchiveContentFormat.OTHER,
        "htm": CombineArchiveContentFormat.OTHER,
        "xul": CombineArchiveContentFormat.OTHER,
        "c": CombineArchiveContentFormat.OTHER,
        "exf": CombineArchiveContentFormat.OTHER,
        "cmgui": CombineArchiveContentFormat.OTHER,
        "doc": CombineArchiveContentFormat.OTHER,
        "exnode": CombineArchiveContentFormat.OTHER,
        "exelem": CombineArchiveContentFormat.OTHER,
        "cpp": CombineArchiveContentFormat.OTHER,
        "msh": CombineArchiveContentFormat.OTHER,
        "vm": CombineArchiveContentFormat.OTHER,
        "coordinates": CombineArchiveContentFormat.TEXT,
        "connectivity": CombineArchiveContentFormat.TEXT,
        "orig": CombineArchiveContentFormat.OTHER,
        "README": CombineArchiveContentFormat.TEXT,
        "css": CombineArchiveContentFormat.OTHER,
        "psd": CombineArchiveContentFormat.OTHER,
        "php": CombineArchiveContentFormat.OTHER,
        "LICENSE": CombineArchiveContentFormat.TEXT,
        "cgi": CombineArchiveContentFormat.OTHER,
        "pl": CombineArchiveContentFormat.OTHER,
        "odt": CombineArchiveContentFormat.OTHER,
        "java": CombineArchiveContentFormat.OTHER,
        "ico": CombineArchiveContentFormat.OTHER,
        "log": CombineArchiveContentFormat.TEXT,
        "graphml": CombineArchiveContentFormat.OTHER,
        "class": CombineArchiveContentFormat.OTHER,
        "classpath": CombineArchiveContentFormat.OTHER,
        "prefs": CombineArchiveContentFormat.OTHER,
        "kss": CombineArchiveContentFormat.OTHER,
        "dig": CombineArchiveContentFormat.OTHER,
        "mat": CombineArchiveContentFormat.MATLAB,
        "owl": CombineArchiveContentFormat.OTHER,
        "db": CombineArchiveContentFormat.OTHER,
        "jar": CombineArchiveContentFormat.OTHER,
        "sh": CombineArchiveContentFormat.OTHER,
        "mov": CombineArchiveContentFormat.OTHER,
        "swf": CombineArchiveContentFormat.OTHER,
        "xsl": CombineArchiveContentFormat.OTHER,
        "as": CombineArchiveContentFormat.OTHER,
        # Todo filer these?
        "iml": CombineArchiveContentFormat.OTHER,
        "pyc": CombineArchiveContentFormat.OTHER,
        "gitignore": CombineArchiveContentFormat.TEXT,
    }

    if(file_extension in file_endings_to_format):
        file_format = file_endings_to_format[file_extension]
    else:
        print("Unknown file format:", file_extension)
        file_format = CombineArchiveContentFormat.OTHER
    return file_format


def get_journal_info(metadata, out_path):
    journal_article = None
    journal_article_authors = []
    if(metadata['citation']['identifier']):
        journal_path = out_path + "/journal.json"
        if(os.path.isfile(journal_path)):

            journal_article = json.load(open(journal_path))

            journal_article = JournalArticle(**journal_article)

            journal_article_authors = journal_article.authors

        else:
            pmid = metadata['citation']['identifier']
            print(metadata["identifier"])
            print(pmid)
            # Handle case of https://models.physiomeproject.org/exposure/9d48e39f893b5f1e98e53778f606c2c2/bhalla_iyengar_1999_j.cellml/view
            if(pmid == "urn:miriam:pubmed:99105994"):
                pmid = "urn:miriam:pubmed:9888852"
            if(pmid == "urn:miriam:pubmed:10545344"):
                pmid = "urn:miriam:pubmed:20540926"

            # Handle https://models.physiomeproject.org/exposure/e65479dfe400c330c9087cbdbfc5f9bf/bakker_mensonides_teusink_vanhoek_michels_westerhoff_2000.cellml/view
            if(pmid == "urn:miriam:pubmed:2000-02-29"):
                pmid = "urn:miriam:pubmed:10681445"
            pmid = pmid.split(":")[-1]
            # print("pmid:",pmid)
            # print()

            time.sleep(ENTREZ_DELAY)
            # Temporary handle case when pmid is 11368770 due to wierdness in enterez DOI
            if(pmid != "None" and pmid != "" and pmid != "11368770" and pmid != "8713663"):
                journal_article = get_reference(pmid)
                journal_article_authors = journal_article.authors
                with open(journal_path, "w") as f:
                    json.dump(asdict(journal_article), f, indent=4)
            else:
                journal_article = None
                journal_article_authors = []
    return journal_article, journal_article_authors


def make_omex_metadata(metadata, journal_article, journal_article_authors):

    # Todo default contributor to file/config
    contributors = [{
        "label": "Bilal Shaikh",
        "uri": 'http://identifiers.org/orcid:0000-0001-5801-5510'

    }]
    model_author = metadata['authors']
    if(model_author):
        contributors.append({
            "label": model_author,
            "uri": None
        })

    creators = []
    for author in journal_article_authors:
        creators.append({
            "label": author,
            "uri": None
        })

    thumbnails = [file.split("/")[-1] for file in metadata["thumbnails"]]
    citations = []
    if(journal_article):
        citations = [{
            "label": journal_article.get_citation(),
            "uri": "https://identifiers.org/doi/" + journal_article.doi if journal_article.doi else None
        }]

    project_id = metadata['identifier']
    if(len(project_id) == 32):
        identifier_uri = "https://identifiers.org/pmr:{}".format(project_id)
    else:
        identifier_uri = "https://models.physiomeproject.org/e/{}".format(
            project_id)

    omex_metadata = [{
        'uri': '.',
        "combine_archive_uri": BIOSIMULATIONS_ROOT_URI_FORMAT.format(metadata["identifier"]),
        "title": metadata["title"],
        "thumbnails": thumbnails,
        "abstract": None,
        "keywords": [tag[-1] for tag in (metadata["tags"] or []) if tag is not None and len(tag) > 1],
        "description": metadata["description"],
        "license": {
            "uri": "https://creativecommons.org/licenses/by/3.0/",
            "label": "CC BY 3.0",
        },
        "contributors": contributors,
        "creators": creators,
        'identifiers': [{
            "label": "PMR",
            "uri": identifier_uri
        }],
        'predecessors': [],
        'successors': [],
        'see_also': [],
        'funders': [],
        'other':[],
        'citations': citations

    }]

    return omex_metadata


def process(metadata, project_path):
    logger = logging.getLogger(__name__)

    # Clear output
    # Set up omex archive root folder
    project_id = metadata["identifier"]

    project_out_dir = os.path.join(OUT_DIR, project_id)
    os.makedirs(project_out_dir, exist_ok=True)

    # Workspace for project
    workspace_path = project_path + "/workspace"

    # New folder for Omex root
    contents_path = project_out_dir + "/contents"
    # Clear contents folder if exists
    shutil.rmtree(contents_path, ignore_errors=True)
    combine_archive_path = f'{project_out_dir}/{project_id}.omex'

    # Copy workspace to new directory for omex root
    shutil.copytree(workspace_path, contents_path)

    combine_contents = []
    has_sedml = False
    for root, dirs, files in os.walk(contents_path):

        for content in files:
            file_ending = content.split(".")[-1]
            if(file_ending == "DS_Store"):
                continue
            if(file_ending == "hgsub"):
                continue
            if(file_ending == "session"):
                continue
            content_rel_dir = os.path.relpath(root, contents_path )
            content_rel_path = os.path.join(content_rel_dir, content)
            content_rel_path = content_rel_path.replace("./", "")
            file_format = get_content_format_from_file_extension(file_ending)
            is_sedml = file_format == CombineArchiveContentFormat.SED_ML
            if(is_sedml):
                has_sedml = True

            combine_content = CombineArchiveContent(
                content_rel_path, file_format, is_sedml)
            combine_contents.append(combine_content)

    # Get Journal Info
    journal_article, journal_article_authors = get_journal_info(
        metadata, project_out_dir)

    # create omex metadata
    omex_metadata = make_omex_metadata(
        metadata, journal_article, journal_article_authors)

    # write omex metadata to combine root
    metadata_file, errors, warning = write_metadata(
        omex_metadata, contents_path)
    # write metadata to output file as well
    write_metadata(omex_metadata, project_out_dir)
    # add metadata to contents
    metadata_content = CombineArchiveContent(
        "metadata.rdf", CombineArchiveContentFormat.OMEX_METADATA)
    combine_contents.append(metadata_content)

    # Write combine archive
    combine_archive = CombineArchive(
        contents=combine_contents,)

    combine_writer.run(combine_archive, contents_path, combine_archive_path)
    if(has_sedml):
        os.makedirs("archive", exist_ok=True)
        # Temporary to make uploading to biosimulations easier
        path = "archive/{}.zip".format(project_id)
        combine_writer.run(combine_archive, contents_path, path)
    # Remove combine input directory
    shutil.rmtree(contents_path, ignore_errors=True)

    project_info = {
        "identifier": project_id,
        "title": metadata["title"],
        "has_sedml": has_sedml,
        "has_journal": journal_article is not None,
        "combine_archive_path": combine_archive_path,
        "errors": errors,
    }

    return project_info


def write_metadata(metadata, project_out_dir):

    config = Config(
        OMEX_METADATA_OUTPUT_FORMAT=OmexMetadataOutputFormat.rdfxml)

    BiosimulationsOmexMetaWriter().run(metadata, project_out_dir +
                                       "/metadata.rdf", config=config)
    metadata_file = project_out_dir+"/metadata.rdf"
    _, errors, warnings = BiosimulationsOmexMetaReader().run(metadata_file)

    return metadata_file, errors, warnings
