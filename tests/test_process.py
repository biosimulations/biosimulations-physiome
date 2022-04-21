from sympy import true
from biosimulations_physiome.process_projects import get_cell_ml_files_in_path, get_non_imported_files
import pytest


def test_get_cell_ml_files_in_path():
    cell_ml_files = get_cell_ml_files_in_path(
        "tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace")
    assert len(cell_ml_files) == 6
    assert cell_ml_files == ['tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/environment.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/circulation.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/units.cellml',
                             'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/parameters.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/guyton_circulatory_dynamics_2008.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/circulation_parent.cellml']


def test_process_imports():
    non_imported_files = get_non_imported_files("tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace",
                                                ['tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/environment.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/circulation.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/units.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/parameters.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/guyton_circulatory_dynamics_2008.cellml', 'tests/fixtures/projects/e1f152d0dbd1dec4111faa117db85bc0/workspace/circulation_parent.cellml'])

    assert "units.cellml" not in non_imported_files
    assert "environment.cellml" not in non_imported_files
    assert "parameters.cellml" not in non_imported_files
    assert "circulation.cellml" not in non_imported_files
    assert "guyton_circulatory_dynamics_2008.cellml" in non_imported_files
    assert "circulation_parent.cellml" in non_imported_files
