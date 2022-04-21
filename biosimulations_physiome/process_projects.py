import shutil
import time
from dataclasses import dataclass, asdict
from typing import List
import xml.etree.ElementTree as ET
from lxml import etree
import datetime

import Bio  # type: ignore
from biosimulators_utils.combine.data_model import CombineArchive, CombineArchiveContent, CombineArchiveContentFormat   # type: ignore
from biosimulators_utils.combine.io import CombineArchiveWriter  # type: ignore
from biosimulators_utils.config import Config  # type: ignore
from biosimulators_utils.omex_meta.data_model import BIOSIMULATIONS_ROOT_URI_FORMAT, OmexMetadataOutputFormat  # type: ignore
from biosimulators_utils.omex_meta.io import BiosimulationsOmexMetaWriter, BiosimulationsOmexMetaReader  # type: ignore
from biosimulators_utils.ref.data_model import Reference, JournalArticle  # type: ignore
from biosimulators_utils.ref.utils import get_reference  # type: ignore
from biosimulators_utils.sedml.data_model import (  # type: ignore
    SedDocument, Model, ModelLanguage, UniformTimeCourseSimulation,
    Task, DataGenerator, Report, DataSet,  Variable, DataGenerator, Report, DataSet, Plot, Plot2D, Curve, Surface)
import copy
from biosimulators_utils.sedml.io import SedmlSimulationWriter  # type: ignore
from biosimulators_utils.sedml.model_utils import get_parameters_variables_outputs_for_simulation  # type: ignore

from biosimulators_utils.warnings import BioSimulatorsWarning  # type: ignore
import os
import json
from loguru import logger


OUT_DIR = "out"

Bio.Entrez.email = os.getenv('ENTREZ_EMAIL', None)
ENTREZ_DELAY = 0.5


combine_writer = CombineArchiveWriter()
#logger.add("out.log", backtrace=True,  level="ERROR")


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
        "svgz": CombineArchiveContentFormat.SVGZ,

        # TODO add the formats to biosimulators_utils ( see)

        "dll": CombineArchiveContentFormat.DLL,
        "so": CombineArchiveContentFormat.SO,
        "conf": CombineArchiveContentFormat.TEXT,
        "rb": CombineArchiveContentFormat.RUBY,
        "docx": CombineArchiveContentFormat.DOCX,
        "rtf": CombineArchiveContentFormat.TEXT,
        "RTF": CombineArchiveContentFormat.TEXT,
        "pptx": CombineArchiveContentFormat.PPTX,
        "xls": CombineArchiveContentFormat.XLSX,
        "eps": CombineArchiveContentFormat.EPS,
        "js": CombineArchiveContentFormat.JAVASCRIPT,
        "ai": CombineArchiveContentFormat.AI,
        "html": CombineArchiveContentFormat.HTML,
        "htm": CombineArchiveContentFormat.HTML,
        "xul": CombineArchiveContentFormat.XUL,
        "c": CombineArchiveContentFormat.OTHER,
        "exf": CombineArchiveContentFormat.OTHER,
        "cmgui": CombineArchiveContentFormat.OTHER,
        "doc": CombineArchiveContentFormat.DOC,
        "exnode": CombineArchiveContentFormat.OTHER,
        "exelem": CombineArchiveContentFormat.OTHER,
        "cpp": CombineArchiveContentFormat.CPP_SOURCE,
        "msh": CombineArchiveContentFormat.OTHER,
        "vm": CombineArchiveContentFormat.OTHER,
        "coordinates": CombineArchiveContentFormat.TEXT,
        "connectivity": CombineArchiveContentFormat.TEXT,
        "orig": CombineArchiveContentFormat.OTHER,
        "README": CombineArchiveContentFormat.TEXT,
        "css": CombineArchiveContentFormat.CSS,
        "psd": CombineArchiveContentFormat.PSD,
        "php": CombineArchiveContentFormat.PHP,
        "LICENSE": CombineArchiveContentFormat.TEXT,
        "cgi": CombineArchiveContentFormat.OTHER,
        "pl": CombineArchiveContentFormat.OTHER,
        "odt": CombineArchiveContentFormat.ODT,
        "java": CombineArchiveContentFormat.JAVA_SOURCE,
        "ico": CombineArchiveContentFormat.ICO,
        "log": CombineArchiveContentFormat.TEXT,
        "graphml": CombineArchiveContentFormat.GRAPHML,
        "class": CombineArchiveContentFormat.JAVA_CLASS,
        "classpath": CombineArchiveContentFormat.JAVA_CLASS,
        "prefs": CombineArchiveContentFormat.TEXT,
        "kss": CombineArchiveContentFormat.OTHER,
        "dig": CombineArchiveContentFormat.OTHER,
        "mat": CombineArchiveContentFormat.MATLAB,
        "owl": CombineArchiveContentFormat.OWL,
        "db": CombineArchiveContentFormat.OTHER,
        "jar": CombineArchiveContentFormat.JAVA_ARCHIVE,
        "sh": CombineArchiveContentFormat.BOURNE_SHELL,
        "mov": CombineArchiveContentFormat.OTHER,
        "swf": CombineArchiveContentFormat.SHOCKWAVE_FLASH,
        "xsl": CombineArchiveContentFormat.XSL,
        "as": CombineArchiveContentFormat.ACTIONSCRIPT,
        # Todo filer these?

    }
    file_endings_to_skip = {
        "iml": CombineArchiveContentFormat.OTHER,
        "pyc": CombineArchiveContentFormat.OTHER,
        "gitignore": CombineArchiveContentFormat.TEXT
    }

    if(file_extension in file_endings_to_skip):
        return None
    if(file_extension in file_endings_to_format):
        file_format = file_endings_to_format[file_extension]
    else:
        logger.warning(f'Unknown file format:, {file_extension or "None"}')
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

    default_contributor = {
        "label": "Bilal Shaikh",
        "uri": 'http://identifiers.org/orcid:0000-0001-5801-5510'

    }
    contributors = []
    model_author = metadata['authors']
    if(model_author):
        contributors.append({
            "label": model_author,
            "uri": None
        })
    contributors.append(default_contributor)
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
        label = "PMR: {}".format(project_id)
    else:
        identifier_uri = "https://models.physiomeproject.org/e/{}".format(
            project_id)
        label = "PMR/e: {}".format(project_id)

    omex_metadata = [{
        'uri': '.',
        "created": datetime.datetime.fromtimestamp(int(metadata['created'].strip())) if metadata.get('created', None) else None,
        "modified": [datetime.datetime.fromtimestamp(int(metadata['last_modified'].strip()))] if metadata.get('last_modified', None) else [],
        "combine_archive_uri": BIOSIMULATIONS_ROOT_URI_FORMAT.format(metadata["identifier"]),
        "title": metadata["title"],
        "thumbnails": thumbnails,
        "abstract": None,
        "keywords": [tag[-1] for tag in (metadata["tags"] or []) if tag is not None and len(tag) > 1],
        "description": metadata["description"].strip() if metadata.get("description", None) else None,
        "license": {
            "uri": "https://creativecommons.org/licenses/by/3.0/",
            "label": "CC BY 3.0",
        },
        "contributors": contributors,
        "creators": creators,
        'identifiers': [{
            "label": label,
            "uri": identifier_uri
        }],
        'predecessors': [],
        'successors': [],
        'see_also': [],
        'funders': [],
        'other':[],
        'citations': citations

    }]
    child_metadata = getChildMetadata(metadata)
    omex_metadata = omex_metadata + child_metadata

    return omex_metadata


def getChildMetadata(metadata) -> List:
    child_metadatas = []
    for contentMetadata in (metadata["content_metadata"] or []):
        child_metadata = {
            "combine_archive_uri": BIOSIMULATIONS_ROOT_URI_FORMAT.format(metadata["identifier"]),
            "uri": contentMetadata["file_name"],
            "title": contentMetadata["title"],
            "thumbnails": contentMetadata["thumbnails"] or [],
            "description": contentMetadata["description"].strip() if contentMetadata["description"] else None,
            "license": {
                "uri": "https://creativecommons.org/licenses/by/3.0/",
                "label": "CC BY 3.0",
            }}
        child_metadatas.append(child_metadata)
    return child_metadatas


def process(metadata, project_path):
    errors = []
    # Clear output
    # Set up omex archive root folder
    project_id = metadata["identifier"]

    project_out_dir = os.path.join(OUT_DIR, project_id)
    print(project_out_dir)
    os.makedirs(project_out_dir, exist_ok=True)

    # Workspace for project
    workspace_path = project_path + "/workspace"

    # New folder for Omex root
    contents_path = project_out_dir + "/contents"
    # Clear contents folder if exists
    shutil.rmtree(contents_path, ignore_errors=True)
    combine_archive_path = f'{project_out_dir}/{project_id}.omex'

    # Copy workspace to new directory for omex root
    if os.path.exists(workspace_path):
        shutil.copytree(workspace_path, contents_path)
    else:
        logger.warning("No workspace found for project {}".format(project_id))

    combine_contents = []
    has_sedml = False
    generated_sedml = False
    sedml_files = []
    for root, dirs, files in os.walk(contents_path):

        for content in files:
            # Do not include manifests since we are generating them
            if(content == "manifest.xml"):
                continue
            file_ending = content.split(".")[-1]
            if(file_ending == "DS_Store"):
                continue
            if(file_ending == "hgsub"):
                continue
            if(file_ending == "session"):
                continue
            content_rel_dir = os.path.relpath(root, contents_path)
            content_rel_path = os.path.join(content_rel_dir, content)
            content_rel_path = content_rel_path.replace(
                "./", "")
            file_format = get_content_format_from_file_extension(file_ending)
            if not file_format:
                logger.warning("Skipped file {}".format(content))
                continue

            # Some sedml files or cellml files do not have correct file extension
            is_unspecified_xml = file_format == CombineArchiveContentFormat.XML

            if(is_unspecified_xml):

                try:
                    tree = ET.parse(os.path.join(root, content))
                    xml_root = tree.getroot()

                    # check if root is a model 

                    if xml_root.tag.endswith("model"):
                        logger.debug("Found CellML file {}".format(content))
                        file_format = CombineArchiveContentFormat.CellML
                    # check if root is sedML

                    elif xml_root.tag.endswith("sedML"):
                        logger.debug("Found SED-ML file {}".format(content))
                        file_format = CombineArchiveContentFormat.SED_ML
                except Exception as e:
                    logger.warning(
                        "Could not parse XML file {}".format(content))
                    logger.warning(e)
            is_cellml = file_format == CombineArchiveContentFormat.CellML
            if(is_cellml):
                new_path = correct_cellml_files(project_id, content_rel_path, root)
                
                    
            
            is_sedml = file_format == CombineArchiveContentFormat.SED_ML
            if(is_sedml):
                has_sedml = True
                sedml_files.append(content_rel_path)
                correct_sedml_files(project_id, content_rel_path, root)
            combine_content = CombineArchiveContent(
                content_rel_path, file_format, is_sedml)
            combine_contents.append(combine_content)
            # Get Journal Info
    journal_article, journal_article_authors = get_journal_info(
        metadata, project_out_dir)

    # create omex metadata
    omex_metadata = make_omex_metadata(
        metadata, journal_article, journal_article_authors)

    if(has_sedml):
        pass
    else:
        try:
            identifier = metadata["identifier"]
            sedml_content, sedml_metadata = generate_sedml(
                contents_path, identifier)
            combine_contents = combine_contents + sedml_content
            omex_metadata = omex_metadata + sedml_metadata
            generated_sedml = True
        except(Exception) as e:
            logger.error(
                "Error generating SEDML for project {}: {}".format(project_id, e))
            errors.append(str(e))

        # write omex metadata to combine root
    metadata_file, metadata_errors, warning = write_metadata(
        omex_metadata, contents_path)
    errors = errors + metadata_errors
    # write metadata to output file as well
    write_metadata(omex_metadata, project_out_dir)
    # add metadata to contents
    metadata_content = CombineArchiveContent(
        "metadata.rdf", CombineArchiveContentFormat.OMEX_METADATA)
    combine_contents.append(metadata_content)

    combine_archive = CombineArchive(
        contents=combine_contents,)

    combine_writer.run(combine_archive, contents_path, combine_archive_path)

    # Remove combine input directory
    shutil.rmtree(contents_path, ignore_errors=True)
    project_info = {
        "identifier": project_id,
        "title": metadata["title"],
        "description": (metadata["description"] or "").strip(),
        "has_sedml": has_sedml,
        "generated_sedml": generated_sedml,
        "has_journal": journal_article is not None,
        "combine_archive_path": combine_archive_path,
        "errors": errors,
    }

    return project_info


def correct_cellml_files(project_id, rel_path, root):
    if(rel_path.endswith(".cellml")):
        filename = rel_path.split(".cellml")[0]
        
            
    
    if project_id=="f17a3cade0f0f7986b060b8bbf5c2957" or project_id=="1a":
        cellml_file = os.path.join(root, rel_path)
        cellml_file_content = open(cellml_file, "r").read()
        cellml_file_content = cellml_file_content.replace("http://www.w3.org/1999/0P/PP-rdf-syntax-ns#", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        open(cellml_file, "w").write(cellml_file_content)
    


def correct_sedml_files(project_id, rel_path, root):

    if project_id == "4a6" and rel_path == "simulation-experiment.sedml":
        sedml_file = os.path.join(root, rel_path)
        sedml_file_content = open(sedml_file, "r").read()
        sedml_file_content = sedml_file_content.replace(
            "source=\"Boron CO2 expts - original eqns - SS--RO--PH.cellml\"", "source=\"model.cellml\"")
        open(sedml_file, "w").write(sedml_file_content)


def generate_sedml(contents_path, identifier) -> List[CombineArchiveContent]:
    cellml_files = get_cell_ml_files_in_path(contents_path)

    non_imported_files = get_non_imported_files(contents_path, cellml_files)

    if len(non_imported_files) == 0:
        raise Exception("No non imported files found")
    contents = []
    metadatas = []
    for index, cellml_file in enumerate(non_imported_files):
        logger.debug("Generating SED-ML for {}".format(cellml_file))

        # Rewrite cellml file to remove all groups to enable SED-ML to use xpaths with opencor python interface
        tree = etree.parse(os.path.join(contents_path, cellml_file))
        root = tree.getroot()
        groups = []
        for child in root:
            if(child.tag == "{http://www.cellml.org/cellml/1.0#}group"):

                groups.append(child)
            if(child.tag == "{http://www.cellml.org/cellml/1.1#}group"):

                groups.append(child)
        for group in groups:
            logger.debug("Removing group {}".format(group))
            root.remove(group)

        tree.write(os.path.join(contents_path, cellml_file),
                   encoding="utf-8", xml_declaration=True)

        # create  sed document for the model
        params,  sims, vars, plots = get_parameters_variables_outputs_for_simulation(
            contents_path + "/" + cellml_file, ModelLanguage.CellML, UniformTimeCourseSimulation, "KISAO_0000019", model_language_options={
                ModelLanguage.CellML: {
                    "observable_only": True,
                }
            })
        if(len(vars) > 0):

            sedml_doc = SedDocument()
            logger.debug(f"Creating SED-ML document for {cellml_file}")

            model = Model(
                id='model',
                source=cellml_file,
                language=ModelLanguage.CellML.value,
                changes=params,
            )
            sedml_doc.models.append(model)
            for i_sim, sim in enumerate(sims):
                sedml_doc.simulations.append(sim)

                if len(sims) > 1:
                    sim_suffix = '_' + str(i_sim)
                else:
                    sim_suffix = ''

                task = Task(
                    id='task' + sim_suffix,
                    model=model,
                    simulation=sim,
                )
                sedml_doc.tasks.append(task)

                report = Report(
                    id='report' + sim_suffix,
                )
                sedml_doc.outputs.append(report)

                var_data_gen_map = {}

                for var in vars:
                    var_copy = copy.copy(var)
                    var_copy.id = '{}{}'.format(var_copy.id, sim_suffix)
                    var_copy.task = task
                    logger.debug(f"Adding variable {var_copy.id} to report")

                    data_gen = DataGenerator(
                        id='data_generator{}_{}'.format(
                            sim_suffix, var_copy.id),
                        name=var_copy.name,
                        variables=[var_copy],
                        math=var_copy.id,
                    )
                    sedml_doc.data_generators.append(data_gen)
                    var_data_gen_map[var] = data_gen

                    report.data_sets.append(DataSet(
                        id='data_set{}_{}'.format(sim_suffix, var_copy.id),
                        label=var_copy.id,
                        name=var_copy.name,
                        data_generator=data_gen,
                    ))

                for plot in plots:
                    plot_copy = copy.copy(plot)
                    plot_copy.id = '{}{}'.format(plot_copy.id, sim_suffix)

                    if isinstance(plot, Plot2D):
                        plot_copy.curves = []
                        for curve in plot.curves:
                            assert len(curve.x_data_generator.variables) == 1
                            assert len(curve.y_data_generator.variables) == 1
                            assert curve.x_data_generator.math == curve.x_data_generator.variables[
                                0].id
                            assert curve.y_data_generator.math == curve.y_data_generator.variables[
                                0].id

                            plot_copy.curves.append(Curve(
                                id='{}{}'.format(curve.id, sim_suffix),
                                name=curve.name,
                                x_data_generator=var_data_gen_map[curve.x_data_generator.variables[0]],
                                y_data_generator=var_data_gen_map[curve.y_data_generator.variables[0]],
                                x_scale=curve.x_scale,
                                y_scale=curve.y_scale,
                            ))

                    else:
                        plot_copy.surfaces = []
                        for surface in plot.surfaces:
                            assert len(surface.x_data_generator.variables) == 1
                            assert len(surface.y_data_generator.variables) == 1
                            assert len(surface.z_data_generator.variables) == 1
                            assert surface.x_data_generator.math == surface.x_data_generator.variables[
                                0].id
                            assert surface.y_data_generator.math == surface.y_data_generator.variables[
                                0].id
                            assert surface.z_data_generator.math == surface.z_data_generator.variables[
                                0].id

                            plot_copy.surfaces.append(Surface(
                                id='{}{}'.format(surface.id, sim_suffix),
                                name=surface.name,
                                x_data_generator=var_data_gen_map[surface.x_data_generator.variables[0]],
                                y_data_generator=var_data_gen_map[surface.y_data_generator.variables[0]],
                                z_data_generator=var_data_gen_map[surface.z_data_generator.variables[0]],
                                x_scale=surface.x_scale,
                                y_scale=surface.y_scale,
                                z_scale=surface.z_scale,
                            ))

                    sedml_doc.outputs.append(plot_copy)

            SedmlSimulationWriter().run(sedml_doc, os.path.join(
                contents_path, f'simulation_{index}.sedml'))
            content = CombineArchiveContent(
                f'simulation_{index}.sedml', CombineArchiveContentFormat.SED_ML, True)
            metadata = {
                'uri': f'simulation_{index}.sedml',
                "combine_archive_uri": BIOSIMULATIONS_ROOT_URI_FORMAT.format(identifier),
                "title": f"Simulation {index}",
                "abstract": None,
                "description": f'Automatically generated SED-ML file for model {cellml_file}',
                "license": {
                    "uri": "https://creativecommons.org/licenses/by/4.0/",
                    "label": "CC BY 4.0",
                },
                "contributors": [],
                "creators": [],
                'identifiers': [],
                'predecessors': [{
                    "uri": f'{BIOSIMULATIONS_ROOT_URI_FORMAT.format(identifier)}/{cellml_file}',
                    "label": f'{cellml_file.split(".cellml")[0] if cellml_file.endswith(".cellml") else (cellml_file.split(".xml")[0] if cellml_file.endswith(".xml") else cellml_file)}',
                }

                ],
                'successors': [],
                'see_also': [],
                'funders': [],
                'other': [],
                'citations': []
            }

            contents.append(content)
            metadatas.append(metadata)
        else:
            logger.warning(f"No variables found in {cellml_file}")
    return contents, metadatas


def get_cell_ml_files_in_path(contents_path):
    # get a list of all the files in the contents_path and subdirectories that end in .cellml
    cellml_files = []

    for root, dirs, files in os.walk(contents_path):
        for file in files:
            if file.endswith(".cellml"):
                cellml_files.append(os.path.join(root, file))
            if file.endswith(".xml"):
                tree = ET.parse(os.path.join(root, file))
                xml_root = tree.getroot()
                # check if xml root is a model with xmlns for cellml
                if xml_root.tag.endswith("model"):
                    cellml_files.append(os.path.join(root, file))
    return cellml_files


def get_non_imported_files(contents_path, cellml_files):
    # make a dict of each file name and boolean value of whether it is imported by another file
    is_imported = {}
    non_imported_files = []
    for file in cellml_files:
        dir_path = os.path.realpath(contents_path)

        file_path = os.path.realpath(file)

        rel_file_path = os.path.relpath(file_path, dir_path)

        is_imported[rel_file_path] = False

        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:

            if child.tag == "{http://www.cellml.org/cellml/1.1#}import":
                imported_file = child.attrib.get(
                    "{http://www.w3.org/1999/xlink}href", None)
                if imported_file is not None:
                    is_imported[imported_file] = True

    # make a list of all the files that are not imported
    non_imported_files = [
        file for file in is_imported.keys() if not is_imported[file]]

    return non_imported_files


def write_metadata(metadata, project_out_dir):

    config = Config(
        OMEX_METADATA_OUTPUT_FORMAT=OmexMetadataOutputFormat.rdfxml)
    os.makedirs(project_out_dir, exist_ok=True)
    BiosimulationsOmexMetaWriter().run(metadata, project_out_dir +
                                       "/metadata.rdf", config=config)
    metadata_file = project_out_dir+"/metadata.rdf"
    _, errors, warnings = BiosimulationsOmexMetaReader().run(metadata_file)

    return metadata_file, errors, warnings
