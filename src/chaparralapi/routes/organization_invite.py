from typing import Optional, Dict

from ..constants import DEFAULT_BASE_URL, DEFAULT_ORGANIZATION_INVITE_ENDPOINT
from .base import post


def create_organization_invite(token: str, data: Dict[str, str], base_url: str = DEFAULT_BASE_URL,
                               timeout: Optional[int] = None) -> None:
    raise NotImplementedError("This function is not implemented yet. Requires Admin permissions.")

    url = f"{base_url}/{DEFAULT_ORGANIZATION_INVITE_ENDPOINT}"
    return post(token, url, data, timeout)