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
