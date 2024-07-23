import pytest
from chaparralapi import client
from requests.models import Response
import json


@pytest.fixture
def api():
    token = 'XXXXXX'
    return client.Client(token)


def mocked_response(data, status_code=200):
    response = Response()
    response.status_code = status_code
    response._content = json.dumps(data).encode('utf-8')
    return response


def test_get_all_projects(api, mocker):
    mock_data = [
        {
            "user_id": "user123",
            "organization_id": "org123",
            "id": "proj123",
            "name": "Test Project",
            "description": "A test project",
            "tags": ["test", "project"],
            "created_at": "2024-05-15T12:00:00Z"
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    projects = api.get_projects()
    assert len(projects) == 1
    assert projects[0].id == "proj123"


def test_get_project(api, mocker):
    project_id = "proj123"
    mock_data = {
        "user_id": "user123",
        "organization_id": "org123",
        "id": project_id,
        "name": "Test Project",
        "description": "A test project",
        "tags": ["test", "project"],
        "created_at": "2024-05-15T12:00:00Z"
    }
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    project = api.get_project(project_id)
    assert project.id == project_id


def test_create_project(api, mocker):
    mock_data = {
        "user_id": "user123",
        "organization_id": "org123",
        "id": "proj124",
        "name": "New Project",
        "description": "New Description",
        "tags": ["new", "project"],
        "created_at": "2024-05-15T12:00:00Z"
    }
    mocker.patch('requests.post', return_value=mocked_response(mock_data, 201))
    new_proj = api.create_project('New Project', 'New Description')
    assert new_proj.id == "proj124"


def test_update_project(api, mocker):
    project_id = "proj123"
    mock_data = {
        "user_id": "user123",
        "organization_id": "org123",
        "id": project_id,
        "name": "Updated Project",
        "description": "Updated Description",
        "tags": ["updated", "project"],
        "created_at": "2024-04-15T12:00:00Z",
        "updated_at": "2024-05-15T12:10:00Z"
    }
    mock_get_data = {
        "user_id": "user123",
        "organization_id": "org123",
        "id": project_id,
        "name": "Project",
        "description": "Description",
        "tags": ["updated"],
        "created_at": "2024-04-15T12:00:00Z",
        "updated_at": "2024-04-15T12:10:00Z"
    }
    mocker.patch('requests.put', return_value=mocked_response(mock_data))
    mocker.patch('requests.get', return_value=mocked_response(mock_get_data))
    updated_proj = api.update_project(project_id, 'Updated Project', 'Updated Description', ['updated'])
    assert updated_proj.id == project_id
    assert updated_proj.name == "Updated Project"


def test_delete_project(api, mocker):
    project_id = "proj124"
    mocker.patch('requests.delete', return_value=mocked_response({}, 204))
    api.delete_project(project_id)


def test_get_organization(api, mocker):
    mock_data = {
        "id": "org123",
        "name": "Test Organization",
        "created_at": "2024-05-15T12:00:00Z",
        "updated_at": "2024-05-16T12:00:00Z"
    }
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    organization = api.get_organization()
    assert organization.id == "org123"


def test_get_all_fastas(api, mocker):
    mock_data = [
        {
            "id": "fasta123",
            "name": "Test Fasta",
            "crc32": 123456,
            "size": 1000,
            "protein_count": 500,
            "organism": "Human",
            "decoy_tag": "DECOY",
            "key": "fasta_key",
            "organization_id": "org123"
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    fastas = api.get_databases()
    assert len(fastas) == 1
    assert fastas[0].id == "fasta123"


def test_get_fasta(api, mocker):
    fasta_id = "fasta123"
    mock_data = {
        "id": fasta_id,
        "name": "Test Fasta",
        "crc32": 123456,
        "size": 1000,
        "protein_count": 500,
        "organism": "Human",
        "decoy_tag": "DECOY",
        "key": "fasta_key",
        "organization_id": "org123"
    }
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    fasta = api.get_database(fasta_id)
    assert fasta.id == fasta_id


def test_update_fasta(api, mocker):
    fasta_id = "fasta123"
    mock_data = {
        "id": fasta_id,
        "name": "Updated Fasta",
        "crc32": 123456,
        "size": 1000,
        "protein_count": 500,
        "organism": "Mouse",
        "decoy_tag": "DECOY",
        "key": "fasta_key",
        "organization_id": "org123"
    }
    mocker.patch('requests.put', return_value=mocked_response(mock_data))
    updated_fasta = api.update_database(fasta_id, "Updated Fasta", "Mouse", "DECOY")
    assert updated_fasta.name == "Updated Fasta"
    assert updated_fasta.organism == "Mouse"



def test_delete_fasta(api, mocker):
    fasta_id = "fasta124"
    mocker.patch('requests.delete', return_value=mocked_response({}, 204))
    api.delete_database(fasta_id)


def test_get_all_search_results(api, mocker):
    mock_data = [
        {
            "id": "sr123",
            "notes": "Test search result",
            "passing_psms": 10,
            "passing_peptides": 20,
            "passing_proteins": 5,
            "input_files": ["file1", "file2"],
            "params": {'chimera': False, 'database': {'bucket_size': None, 'decoy_tag': None, 'enzyme': {'c_terminal': True, 'cleave_at': 'KR', 'max_len': 30, 'min_len': 7, 'missed_cleavages': 1, 'restrict': None}, 'fasta': 'fasta_067P9PD0WC3B9P1T60F57GG1B4', 'fragment_max_mz': None, 'fragment_min_mz': None, 'generate_decoys': None, 'ion_kinds': None, 'max_variable_mods': None, 'min_ion_index': None, 'peptide_max_mass': None, 'peptide_min_mass': None, 'static_mods': {'C': 57.021461486816406}, 'variable_mods': {'M': [15.994915008544922]}}, 'deisotope': True, 'fragment_tol': {'ppm': [-10, 10]}, 'isotope_errors': [-1, 3], 'linear_model': {'contrasts': [], 'designs': [{'filename': 'QEX3_1170178', 'group': '?', 'tmt_channel': None}]}, 'max_fragment_charge': 1, 'max_peaks': 150, 'min_matched_peaks': 4, 'min_peaks': 15, 'mzml_paths': None, 'output_directory': None, 'precursor_tol': {'ppm': [-50, 50]}, 'predict_rt': True, 'quant': {'lfq': False, 'lfq_settings': {'ppm_tolerance': 5}, 'tmt': None, 'tmt_settings': {'level': 3}}, 'report_psms': 1, 'wide_window': False, 'write_pin': None},
            "project_id": "proj123",
            "project_name": "Test Project",
            "organization_id": "org123",
            "job_id": "job123",
            "created_at": "2024-05-15T12:00:00Z",
            "started_at": "2024-05-15T12:10:00Z",
            "finished_at": "2024-05-15T13:00:00Z",
            "status": "SUCCEEDED",
            "cpu": 4,
            "memory": 16
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    search_results = api.get_search_results()
    assert len(search_results) == 1
    assert search_results[0].id == "sr123"


def test_get_search_result_download(api, mocker):
    search_result_id = "sr123"
    mock_data = {
        "config.json": "https://example.com/config.json",
        "matched_fragments.sage.parquet": "https://example.com/matched_fragments.sage.parquet",
        "peptide.csv": "https://example.com/peptide.csv",
        "proteins.csv": "https://example.com/proteins.csv",
        "results.json": "https://example.com/results.json",
        "results.sage.parquet": "https://example.com/results.sage.parquet"
    }
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    search_result_download = api.get_search_result_download(search_result_id)
    assert search_result_download.config_json == "https://example.com/config.json"


def test_get_qc_scores(api, mocker):
    search_result_id = "sr123"
    mock_data = [
        {
            "bin": 0.5,
            "count": 100,
            "is_decoy": True
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    qc_scores = api.get_qc_scores(search_result_id)
    assert len(qc_scores) == 1
    assert qc_scores[0].bin == 0.5


def test_get_qc_ids(api, mocker):
    search_result_id = "sr123"
    mock_data = [
        {
            "filename": "test_file",
            "peptides": 10,
            "protein_groups": 5,
            "psms": 20
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    qc_ids = api.get_qc_ids(search_result_id)
    assert len(qc_ids) == 1
    assert qc_ids[0].filename == "test_file"


def test_get_qc_precursors(api, mocker):
    search_result_id = "sr123"
    mock_data = [
        {
            "filename": "test_file",
            "q10": 0.1,
            "q25": 0.25,
            "q50": 0.5,
            "q75": 0.75,
            "q90": 0.9
        }
    ]
    mocker.patch('requests.get', return_value=mocked_response(mock_data))
    qc_precursors = api.get_qc_precursors(search_result_id)
    assert len(qc_precursors) == 1
    assert qc_precursors[0].q10 == 0.1


if __name__ == "__main__":
    pytest.main()
