from typing import Optional, List, Dict, Any

from ..constants import DEFAULT_BASE_URL, DEFAULT_PROJECTS_ENDPOINT
from .base import get, post, put, delete


def get_projects(token: str, base_url: str = DEFAULT_BASE_URL,
                 timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}"
    projects_data = get(token, url, timeout)
    return projects_data


def get_project(token: str, project_id: str, base_url: str = DEFAULT_BASE_URL,
                timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}"
    project_data = get(token, url, timeout)
    return project_data


def create_project(token: str, data: Dict[str, str], base_url: str = DEFAULT_BASE_URL,
                   timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}"
    project_data = post(token, url, data, timeout)
    return project_data


def update_project(token: str, project_id: str, data: Dict[str, str],
                   base_url: str = DEFAULT_BASE_URL,
                   timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}"
    project_data = put(token, url, data, timeout)
    return project_data


def delete_project(token: str, project_id: str, base_url: str = DEFAULT_BASE_URL,
                   timeout: Optional[int] = None) -> None:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}"
    delete(token, url, timeout)
