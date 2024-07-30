from typing import Optional, List, Dict, Any, IO

import requests
from requests import Timeout

from ..constants import DEFAULT_BASE_URL, DEFAULT_PROJECTS_ENDPOINT, DEFAULT_PROJECT_FILES_ENDPOINT
from .base import get


def get_project_files(token: str, project_id: str, base_url: str = DEFAULT_BASE_URL, timeout: Optional[int] = None)\
        -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}/{DEFAULT_PROJECT_FILES_ENDPOINT}"
    return get(token, url, timeout)


def upload_project_file(token: str, project_id: str, file: IO, filename: str,
                        base_url: str = DEFAULT_BASE_URL,
                        timeout: Optional[int] = None) -> None:
    url = f"{base_url}/{DEFAULT_PROJECTS_ENDPOINT}/{project_id}/{DEFAULT_PROJECT_FILES_ENDPOINT}"
    if filename.endswith('.raw'):
        files = {
            'file': (filename, file, 'image/RAW')
        }
    else:
        files = {
            'file': (filename, file, 'application/octet-stream')
        }
    try:
        response = requests.put(url, headers={'Authorization': f'Bearer {token}'}, files=files, timeout=timeout)
        response.raise_for_status()
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc

