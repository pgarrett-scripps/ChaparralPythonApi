from typing import Optional, List, Dict, Any

import requests
from requests import Timeout

from ..constants import DEFAULT_BASE_URL, DEFAULT_DATABASES_ENDPOINT
from .base import get, put, delete


def get_databases(token: str, base_url: str = DEFAULT_BASE_URL,
                  timeout: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
    url = f"{base_url}/{DEFAULT_DATABASES_ENDPOINT}"
    return get(token, url, timeout)


def get_database(token: str, database_id: str, base_url: str = DEFAULT_BASE_URL,
                 timeout: Optional[int] = None) -> Optional[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_DATABASES_ENDPOINT}/{database_id}"
    return get(token, url, timeout)


def create_database(token: str, database_bytes: bytes, filename: str,
                    base_url: str = DEFAULT_BASE_URL,
                    timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_DATABASES_ENDPOINT}"
    files = {'file': (filename, database_bytes, 'application/octet-stream')}
    try:
        response = requests.put(url, headers={'Authorization': f'Bearer {token}'}, files=files, timeout=timeout)
        response.raise_for_status()
        return response.json()[0]
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc


def update_database(token: str, database_id: str, data: Dict[str, Any],
                    base_url: str = DEFAULT_BASE_URL,
                    timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_DATABASES_ENDPOINT}/{database_id}"
    return put(token, url, data, timeout)


def delete_database(token: str, database_id: str, base_url: str = DEFAULT_BASE_URL,
                    timeout: Optional[int] = None) -> None:
    url = f"{base_url}/{DEFAULT_DATABASES_ENDPOINT}/{database_id}"
    delete(token, url, timeout)
