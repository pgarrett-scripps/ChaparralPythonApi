from typing import List, Optional

from .fasta import (list_fasta_query, Fasta, read_fasta_query, update_fasta_query,
                    usePresignedFastaMutation)
from .organization import (read_organization_query, update_organiation_query,
                           invite_organization_query, Organization)
from .projects import (Project, update_project_query, creat_project_query, list_project_query,
                       read_project_query)
from .search_results import (list_search_result_query, read_search_result_download_query,
                             SearchResultDownload, SearchResult, QcScore,
                             read_search_result_qc_id_query, read_search_result_qc_precursor_query, QcId,
                             QcPrecursor, read_search_result_qc_score_query)


class MyApi:
    def __init__(self, token: str, base_url: str = 'https://api.us-west.chaparral.ai'):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def list_projects(self) -> List[Project]:
        return list_project_query(self.base_url, self.headers)

    def read_project(self, project_id: str) -> Project:
        return read_project_query(self.base_url, self.headers, project_id)

    def update_project(self, project_id: str, name: str, description: str, tags: List[str] = None) -> Project:
        data = {
            "name": name,
            "description": description,
            "tags": [] if tags is None else tags
        }
        return update_project_query(self.base_url, self.headers, project_id, data)

    def create_project(self, name: str, description: str) -> Project:
        data = {
            "name": name,
            "description": description
        }
        return creat_project_query(self.base_url, self.headers, data)

    def list_fasta(self) -> List[Fasta]:
        return list_fasta_query(self.base_url, self.headers)

    def read_fasta(self, fasta_id: str) -> Fasta:
        return read_fasta_query(self.base_url, self.headers, fasta_id)

    def update_fasta(self, fasta_id: str, name: str, organism: str, decoy_tag: Optional[str]) -> Fasta:
        data = {
            "name": name,
            "organism": organism,
            "decoy_tag": decoy_tag
        }
        return update_fasta_query(self.base_url, self.headers, fasta_id, data)

    def create_fasta(self, fasta_file: str) -> Fasta:
        raise NotImplementedError

        with open(fasta_file, 'rb') as f:
            data = f.read()
            return usePresignedFastaMutation(self.base_url, self.headers, data)

    def read_organization(self) -> Organization:
        return read_organization_query(self.base_url, self.headers)

    def update_organization(self, org_id: str, name: str) -> Organization:
        raise NotImplementedError
        data = {
            "id": org_id,
            "name": name
        }
        return update_organiation_query(self.base_url, self.headers, data)

    def invite_organization(self, email: str) -> Organization:
        raise NotImplementedError

        data = {
            "email": email
        }
        return invite_organization_query(self.base_url, self.headers, data)

    def list_search_results(self) -> List[SearchResult]:
        return list_search_result_query(self.base_url, self.headers)

    def read_search_result_download(self, search_result_id: str) -> SearchResultDownload:
        return read_search_result_download_query(self.base_url, self.headers, search_result_id)

    def get_config_json(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_config_json()

    def get_matched_fragments_parquet(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_matched_fragments_parquet()

    def get_peptide_csv(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_peptide_csv()

    def get_proteins_csv(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_proteins_csv()

    def get_results_json(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_results_json()

    def get_results_parquet(self, search_result_id: str) -> str:
        search_result_download = read_search_result_download_query(self.base_url, self.headers, search_result_id)
        return search_result_download.get_results_parquet()

    def read_search_result_qc_score_query(self, search_id: str) -> List[QcScore]:
        return read_search_result_qc_score_query(self.base_url, self.headers, search_id)

    def read_search_result_qc_id_query(self, search_id: str) -> List[QcId]:
        return read_search_result_qc_id_query(self.base_url, self.headers, search_id)

    def read_search_result_qc_precursor_query(self, search_id: str) -> List[QcPrecursor]:
        return read_search_result_qc_precursor_query(self.base_url, self.headers, search_id)
