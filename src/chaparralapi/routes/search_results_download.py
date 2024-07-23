from typing import Optional, Dict, Any

from ..constants import DEFAULT_BASE_URL, DEFAULT_SEARCH_RESULTS_DOWNLOAD_ENDPOINT, DEFAULT_SEARCH_RESULTS_ENDPOINT
from .base import get


def read_search_result_download(token: str, search_result_id: str, base_url: str = DEFAULT_BASE_URL,
                                timeout: Optional[int] = None) -> Dict[str, Any]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/{DEFAULT_SEARCH_RESULTS_DOWNLOAD_ENDPOINT}"
    download_data = get(token, url, timeout)
    return download_data
