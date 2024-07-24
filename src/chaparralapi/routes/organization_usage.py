from typing import Optional, Dict, Any

from ..constants import DEFAULT_ORGANIZATION_USAGE_ENDPOINT, DEFAULT_BASE_URL, DEFAULT_ORGANIZATION_ENDPOINT
from .base import get


def get_organization_usage(token: str, base_url: str = DEFAULT_BASE_URL,
                           timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_ORGANIZATION_ENDPOINT}/{DEFAULT_ORGANIZATION_USAGE_ENDPOINT}"
    return get(token, url, timeout)
