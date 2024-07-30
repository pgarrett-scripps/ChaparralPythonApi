from typing import Optional, List, Dict, Any

from ..constants import (DEFAULT_BASE_URL, DEFAULT_SEARCH_RESULTS_ENDPOINT, DEFAULT_PROJECTS_ENDPOINT,
                         DEFAULT_SEARCH_ENDPOINT)
from .base import get, delete, post


def create_search(token: str, project_id: str, search_config: Dict[str, Any], base_url: str = DEFAULT_BASE_URL,
                  timeout: Optional[int] = None) -> None:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}/{DEFAULT_SEARCH_ENDPOINT}"
    _ = post(token, url, search_config, timeout)
    return None


def get_search_results(token: str, project_id: Optional[str] = None, base_url: str = DEFAULT_BASE_URL,
                       timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    if project_id:
        url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}"
    else:
        url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}"

    results_data = get(token, url, timeout)
    return results_data


def delete_search_result(token: str, search_result_id: str, base_url: str = DEFAULT_BASE_URL,
                         timeout: Optional[int] = None) -> None:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}"
    delete(token, url, timeout)


def get_peptides_from_protein_id(token: str, search_result_id: str, protein_id: str, base_url: str = DEFAULT_BASE_URL,
                 timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/protein/{protein_id}"
    return get(token, url, timeout)

def get_peptides_from_peptide_id(token: str, search_result_id: str, peptide_id: str, base_url: str = DEFAULT_BASE_URL,
                    timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/peptide/{peptide_id}"
    return get(token, url, timeout)


def get_psm_annotations(token: str, search_result_id: str, psm_id: int,
                        base_url: str = DEFAULT_BASE_URL, timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/psm_annotation/{psm_id}"
    return get(token, url, timeout)


def get_spectra(token: str, search_result_id: str, filename: str, scannr: str, base_url: str = DEFAULT_BASE_URL,
                timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/{filename}/{scannr}/mzparquet"
    return get(token, url, timeout)
