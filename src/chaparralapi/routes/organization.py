from typing import Optional, Dict, Any

from ..constants import DEFAULT_BASE_URL, DEFAULT_ORGANIZATION_ENDPOINT
from .base import get, put


def get_organization(token: str, base_url: str = DEFAULT_BASE_URL, timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_ORGANIZATION_ENDPOINT}"
    return get(token, url, timeout)


def update_organization(token: str, organization_id: str, data: Dict[str, str],
                        base_url: str = DEFAULT_BASE_URL,
                        timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_ORGANIZATION_ENDPOINT}/{organization_id}"
    return put(token, url, data, timeout)
