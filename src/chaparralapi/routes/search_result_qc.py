from typing import Optional, List, Dict, Any

from ..constants import (DEFAULT_BASE_URL, DEFAULT_SEARCH_RESULTS_ENDPOINT, DEFAULT_SEARCH_RESULTS_SCORE_QC_ENDPOINT,
                         DEFAULT_SEARCH_RESULTS_IDS_QC_ENDPOINT, DEFAULT_SEARCH_RESULTS_PRECURSORS_QC_ENDPOINT)
from .base import get


def get_qc_scores(token: str, search_result_id: str, base_url: str = DEFAULT_BASE_URL,
                  timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/{DEFAULT_SEARCH_RESULTS_SCORE_QC_ENDPOINT}"
    qc_scores_data = get(token, url, timeout)
    if qc_scores_data is None:
        return []
    return qc_scores_data


def get_qc_ids(token: str, search_result_id: str, base_url: str = DEFAULT_BASE_URL,
               timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/{DEFAULT_SEARCH_RESULTS_IDS_QC_ENDPOINT}"
    qc_ids_data = get(token, url, timeout)
    if qc_ids_data is None:
        return []
    return qc_ids_data


def get_qc_precursors(token: str, search_result_id: str, base_url: str = DEFAULT_BASE_URL,
                      timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    url = (f"{base_url}/{DEFAULT_SEARCH_RESULTS_ENDPOINT}/{search_result_id}/"
           f"{DEFAULT_SEARCH_RESULTS_PRECURSORS_QC_ENDPOINT}")
    qc_precursors_data = get(token, url, timeout)
    if qc_precursors_data is None:
        return []
    return qc_precursors_data
