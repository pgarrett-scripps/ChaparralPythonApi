"""
The Client class is a wrapper around the Chaparral API.
"""

from typing import List, Optional, Dict, Any

import requests
from requests.exceptions import Timeout

from chaparralapi.models import (Project, Organization, Fasta, SearchResult, SearchResultDownload, QcScore, QcId,
                                 QcPrecursor)


class Client:
    """
    The Client class is a wrapper around the Chaparral API.

    :param token: The Chaparral API token.
    :param base_url: The Chaparral API base URL.
    :param timeout: The request timeout in seconds.
    """
    def __init__(self, token: str, base_url: str = 'https://api.us-west.chaparral.ai', timeout: Optional[float] = 10):
        self.token = token
        self.base_url = base_url
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _get(self, endpoint: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        try:
            response = requests.get(url=f"{self.base_url}/{endpoint}",
                                    headers=self.headers,
                                    timeout=timeout or self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout as exc:
            raise Timeout(f'Request to {endpoint} timed out.') from exc

    def _post(self, endpoint: str, data: Dict[str, Any], timeout: Optional[int] = None) -> Dict[str, Any]:
        try:
            response = requests.post(url=f"{self.base_url}/{endpoint}",
                                     headers=self.headers,
                                     json=data,
                                     timeout=timeout or self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout as exc:
            raise Timeout(f'Request to {endpoint} timed out.') from exc

    def _put(self, endpoint: str, data: Dict[str, Any], timeout: Optional[int] = None) -> Dict[str, Any]:
        try:
            response = requests.put(url=f"{self.base_url}/{endpoint}",
                                    headers=self.headers,
                                    json=data,
                                    timeout=timeout or self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout as exc:
            raise Timeout(f'Request to {endpoint} timed out.') from exc

    def _delete(self, endpoint: str, timeout: Optional[int] = None) -> None:
        try:
            response = requests.delete(url=f"{self.base_url}/{endpoint}",
                                       headers=self.headers,
                                       timeout=timeout or self.timeout)
            response.raise_for_status()
        except Timeout as exc:
            raise Timeout(f'Request to {endpoint} timed out.') from exc

    def _fetch_file(self, url: str, timeout: Optional[int] = None) -> str:
        try:
            response = requests.get(url, timeout=timeout or self.timeout)
            response.raise_for_status()
            return response.text
        except Timeout as exc:
            raise Timeout(f'Request to {url} timed out.') from exc

    def get_all_projects(self, timeout: Optional[int] = None) -> List[Project]:
        projects_data = self._get("projects", timeout)
        return [Project.parse_obj(project) for project in projects_data]

    def get_project(self, project_id: str, timeout: Optional[int] = None) -> Project:
        project_data = self._get(f"projects/{project_id}", timeout)
        return Project.parse_obj(project_data)

    def create_project(self, name: str, description: str, timeout: Optional[int] = None) -> Project:
        data = {'name': name, 'description': description}
        project_data = self._post("projects", data, timeout)
        return Project.parse_obj(project_data)

    def update_project(self, project_id: str, name: str, description: str, timeout: Optional[int] = None) -> Project:
        data = {'name': name, 'description': description}
        project_data = self._put(f"projects/{project_id}", data, timeout)
        return Project.parse_obj(project_data)

    def delete_project(self, project_id: str, timeout: Optional[int] = None) -> None:
        self._delete(f"projects/{project_id}", timeout)

    def get_organization(self, timeout: Optional[int] = None) -> Organization:
        organization_data = self._get("organization", timeout)
        return Organization.parse_obj(organization_data)

    def update_organization(self, name: str, timeout: Optional[int] = None) -> Organization:
        data = {'name': name}
        organization_data = self._put("organization", data, timeout)
        return Organization.parse_obj(organization_data)

    def invite_to_organization(self, email: str, timeout: Optional[int] = None) -> None:
        data = {'email': email}
        self._post("organization/invite", data, timeout)

    def get_all_fastas(self, timeout: Optional[int] = None) -> List[Fasta]:
        fastas_data = self._get("databases", timeout)
        return [Fasta.parse_obj(fasta) for fasta in fastas_data]

    def get_fasta(self, fasta_id: str, timeout: Optional[int] = None) -> Fasta:
        fasta_data = self._get(f"databases/{fasta_id}", timeout)
        return Fasta.parse_obj(fasta_data)

    def update_fasta(self, fasta_id: str, name: str, organism: str, decoy_tag: Optional[str],
                     timeout: Optional[int] = None) -> Fasta:
        data = {'name': name, 'organism': organism, 'decoy_tag': decoy_tag}
        fasta_data = self._put(f"databases/{fasta_id}", data, timeout)
        return Fasta.parse_obj(fasta_data)

    def create_fasta(self) -> None:
        raise NotImplementedError

    def delete_fasta(self, fasta_id: str, timeout: Optional[int] = None) -> None:
        self._delete(f"databases/{fasta_id}", timeout)

    def get_all_search_results(self, timeout: Optional[int] = None) -> List[SearchResult]:
        search_results_data = self._get("search_results", timeout)
        return [SearchResult.parse_obj(result) for result in search_results_data]

    def get_search_result_download(self, search_result_id: str, timeout: Optional[int] = None) -> SearchResultDownload:
        search_result_download_data = self._get(f"search_results/{search_result_id}/download", timeout)
        return SearchResultDownload.parse_obj(search_result_download_data)

    def fetch_config_json(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        config_json = self._fetch_file(search_result_download.config_json, timeout)
        return config_json

    def fetch_matched_fragments_parquet(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        matched_fragments_parquet = self._fetch_file(search_result_download.matched_fragments_parquet, timeout)
        return matched_fragments_parquet

    def fetch_peptide_csv(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        peptide_csv = self._fetch_file(search_result_download.peptide_csv, timeout)
        return peptide_csv

    def fetch_proteins_csv(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        proteins_csv = self._fetch_file(search_result_download.proteins_csv, timeout)
        return proteins_csv

    def fetch_results_json(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        results_json = self._fetch_file(search_result_download.results_json, timeout)
        return results_json

    def fetch_results_parquet(self, search_result_id: str, timeout: Optional[int] = None) -> str:
        search_result_download = self.get_search_result_download(search_result_id, timeout)
        results_parquet = self._fetch_file(search_result_download.results_parquet, timeout)
        return results_parquet

    def get_qc_scores(self, search_result_id: str, timeout: Optional[int] = None) -> List[QcScore]:
        qc_scores_data = self._get(f"search_results/{search_result_id}/qc/scores", timeout)
        return [QcScore.parse_obj(score) for score in qc_scores_data]

    def get_qc_ids(self, search_result_id: str, timeout: Optional[int] = None) -> List[QcId]:
        qc_ids_data = self._get(f"search_results/{search_result_id}/qc/ids", timeout)
        return [QcId.parse_obj(qc_id) for qc_id in qc_ids_data]

    def get_qc_precursors(self, search_result_id: str, timeout: Optional[int] = None) -> List[QcPrecursor]:
        qc_precursors_data = self._get(f"search_results/{search_result_id}/qc/precursors", timeout)
        return [QcPrecursor.parse_obj(precursor) for precursor in qc_precursors_data]
