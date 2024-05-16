from typing import List, Optional

import requests

from chaparralapi.models import Project, Organization, Fasta, SearchResult, SearchResultDownload, QcScore, QcId, QcPrecursor
from chaparralapi.util import get_file


class Client:

    def __init__(self, token: str, base_url: str = 'https://api.us-west.chaparral.ai'):
        self.token = token
        self.base_url = base_url

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def _get(self, endpoint: str):
        response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict):
        response = requests.post(f"{self.base_url}/{endpoint}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, data: dict):
        response = requests.put(f"{self.base_url}/{endpoint}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint: str):
        response = requests.delete(f"{self.base_url}/{endpoint}", headers=self.headers)
        response.raise_for_status()
        return None

    def get_all_projects(self) -> List[Project]:
        return [Project.parse_obj(project) for project in self._get("projects")]

    def get_project(self, project_id: str) -> Project:
        return Project.parse_obj(self._get(f"projects/{project_id}"))

    def create_project(self, name: str, description: str) -> Project:
        data = {'name': name, 'description': description}
        return Project.parse_obj(self._post("projects", data))

    def update_project(self, project_id: str, name: str, description: str) -> Project:
        data = {'name': name, 'description': description}
        return Project.parse_obj(self._put(f"projects/{project_id}", data))

    def delete_project(self, project_id: str) -> None:
        self._delete(f"projects/{project_id}")

    def get_organization(self) -> Organization:
        return Organization.parse_obj(self._get("organization"))

    def update_organization(self, name: str) -> Organization:
        data = {'name': name}
        return Organization.parse_obj(self._put("organization", data))

    def invite_to_organization(self, email: str) -> None:
        data = {'email': email}
        self._post("organization/invite", data)

    def get_all_fastas(self) -> List[Fasta]:
        return [Fasta.parse_obj(fasta) for fasta in self._get("databases")]

    def get_fasta(self, fasta_id: str) -> Fasta:
        return Fasta.parse_obj(self._get(f"databases/{fasta_id}"))

    def update_fasta(self, fasta_id: str, name: str, organism: str, decoy_tag: Optional[str]) -> Fasta:
        data = {'name': name, 'organism': organism, 'decoy_tag': decoy_tag}
        return Fasta.parse_obj(self._put(f"databases/{fasta_id}", data))

    def create_fasta(self) -> Fasta:
        raise NotImplementedError

    def delete_fasta(self, fasta_id: str) -> None:
        self._delete(f"databases/{fasta_id}")

    def get_all_search_results(self) -> List[SearchResult]:
        return [SearchResult.parse_obj(result) for result in self._get("search_results")]

    def get_search_result_download(self, search_result_id: str) -> SearchResultDownload:
        return SearchResultDownload.parse_obj(self._get(f"search_results/{search_result_id}/download"))

    def fetch_config_json(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).config_json)

    def fetch_matched_fragments_parquet(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).matched_fragments_parquet)

    def fetch_peptide_csv(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).peptide_csv)

    def fetch_proteins_csv(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).proteins_csv)

    def fetch_results_json(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).results_json)

    def fetch_results_parquet(self, search_result_id: str) -> str:
        return get_file(self.get_search_result_download(search_result_id).results_parquet)

    def get_qc_scores(self, search_result_id: str) -> List[QcScore]:
        return [QcScore.parse_obj(score) for score in self._get(f"search_results/{search_result_id}/qc/scores")]

    def get_qc_ids(self, search_result_id: str) -> List[QcId]:
        return [QcId.parse_obj(qc_id) for qc_id in self._get(f"search_results/{search_result_id}/qc/ids")]

    def get_qc_precursors(self, search_result_id: str) -> List[QcPrecursor]:
        return [QcPrecursor.parse_obj(precursor) for precursor in self._get(f"search_results/{search_result_id}/qc/precursors")]
