from typing import Optional, Dict, Any

from ..constants import DEFAULT_BASE_URL, DEFAULT_PROFILE_ENDPOINT
from .base import get, put


def get_profile(token: str, base_url: str = DEFAULT_BASE_URL,
                timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_PROFILE_ENDPOINT}"
    return get(token, url, timeout)


def update_profile(token: str, data: Dict[str, Any], base_url: str = DEFAULT_BASE_URL,
                   timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_PROFILE_ENDPOINT}"
    return put(token, url, data, timeout)
