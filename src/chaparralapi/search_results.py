import requests

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .util import get_file


@dataclass
class SearchResult:
    id: str
    notes: Optional[str]
    passing_psms: Optional[int]
    passing_peptides: Optional[int]
    passing_proteins: Optional[int]
    input_files: List[str]
    params: Dict[str, Any]
    project_id: str
    project_name: str
    organization_id: str
    job_id: str
    created_at: str
    started_at: str
    finished_at: str
    status: str
    cpu: int
    memory: int
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'SearchResult':
        return cls(
            id=d['id'],
            notes=d.get('notes'),
            passing_psms=d.get('passing_psms'),
            passing_peptides=d.get('passing_peptides'),
            passing_proteins=d.get('passing_proteins'),
            input_files=d['input_files'],
            params=d['params'],
            project_id=d['project_id'],
            project_name=d['project_name'],
            organization_id=d['organization_id'],
            job_id=d['job_id'],
            created_at=d['created_at'],
            started_at=d['started_at'],
            finished_at=d['finished_at'],
            status=d['status'],
            cpu=d['cpu'],
            memory=d['memory'],
            additional_fields={k: v for k, v in d.items() if
                               k not in ['id', 'notes', 'passing_psms', 'passing_peptides', 'passing_proteins',
                                         'input_files', 'params', 'project_id', 'project_name', 'organization_id',
                                         'job_id', 'created_at', 'started_at', 'finished_at', 'status', 'cpu',
                                         'memory']}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'notes': self.notes,
            'passing_psms': self.passing_psms,
            'passing_peptides': self.passing_peptides,
            'passing_proteins': self.passing_proteins,
            'input_files': self.input_files,
            'params': self.params,
            'project_id': self.project_id,
            'project_name': self.project_name,
            'organization_id': self.organization_id,
            'job_id': self.job_id,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'status': self.status,
            'cpu': self.cpu,
            'memory': self.memory,
            **self.additional_fields
        }


@dataclass
class SearchResultDownload:
    config_json: str
    matched_fragments_parquet: str
    peptide_csv: str
    proteins_csv: str
    results_json: str
    results_parquet: str
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> 'SearchResultDownload':
        return SearchResultDownload(
            config_json=d['config.json'],
            matched_fragments_parquet=d['matched_fragments.sage.parquet'],
            peptide_csv=d['peptide.csv'],
            proteins_csv=d['proteins.csv'],
            results_json=d['results.json'],
            results_parquet=d['results.sage.parquet'],
            additional_fields={k: v for k, v in d.items() if
                               k not in ['config.json', 'matched_fragments.sage.parquet', 'peptide.csv', 'proteins.csv',
                                         'results.json', 'results.sage.parquet']}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'config.json': self.config_json,
            'matched_fragments.sage.parquet': self.matched_fragments_parquet,
            'peptide.csv': self.peptide_csv,
            'proteins.csv': self.proteins_csv,
            'results.json': self.results_json,
            'results.sage.parquet': self.results_parquet,
            **self.additional_fields
        }

    def get_config_json(self) -> str:
        return get_file(self.config_json)

    def get_matched_fragments_parquet(self) -> str:
        return get_file(self.matched_fragments_parquet)

    def get_peptide_csv(self) -> str:
        return get_file(self.peptide_csv)

    def get_proteins_csv(self) -> str:
        return get_file(self.proteins_csv)

    def get_results_json(self) -> str:
        return get_file(self.results_json)

    def get_results_parquet(self) -> str:
        return get_file(self.results_parquet)


@dataclass
class QcScore:
    bin: float
    count: int
    is_decoy: bool

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'QcScore':
        return cls(
            bin=d['bin'],
            count=d['count'],
            is_decoy=d['is_decoy']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'bin': self.bin,
            'count': self.count,
            'is_decoy': self.is_decoy
        }


@dataclass
class QcId:
    filename: str
    peptides: int
    protein_groups: int
    psms: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'QcId':
        return cls(
            filename=d['filename'],
            peptides=d['peptides'],
            protein_groups=d['protein_groups'],
            psms=d['psms']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'filename': self.filename,
            'peptides': self.peptides,
            'protein_groups': self.protein_groups,
            'psms': self.psms
        }


@dataclass
class QcPrecursor:
    filename: str
    q10: float
    q25: float
    q50: float
    q75: float
    q90: float

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'QcPrecursor':
        return cls(
            filename=d['filename'],
            q10=d['q10'],
            q25=d['q25'],
            q50=d['q50'],
            q75=d['q75'],
            q90=d['q90']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'filename': self.filename,
            'q10': self.q10,
            'q25': self.q25,
            'q50': self.q50,
            'q75': self.q75,
            'q90': self.q90
        }


def list_search_result_query(base_url: str, headers: Dict) -> List[SearchResult]:
    response = requests.get(f"{base_url}/search_results", headers=headers)
    response.raise_for_status()
    return [SearchResult.from_dict(search_result) for search_result in response.json()]


def read_search_result_download_query(base_url: str, headers: Dict, search_id: str) -> SearchResultDownload:
    response = requests.get(f"{base_url}/search_results/{search_id}/download", headers=headers)
    response.raise_for_status()
    return SearchResultDownload.from_dict(response.json())


def read_search_result_qc_score_query(base_url: str, headers: Dict, search_id: str) -> List[QcScore]:
    response = requests.get(f"{base_url}/search_results/{search_id}/qc/scores", headers=headers)
    response.raise_for_status()
    return [QcScore.from_dict(qc) for qc in response.json()]


def read_search_result_qc_id_query(base_url: str, headers: Dict, search_id: str) -> List[QcId]:
    response = requests.get(f"{base_url}/search_results/{search_id}/qc/ids", headers=headers)
    response.raise_for_status()
    return [QcId.from_dict(qc) for qc in response.json()]


def read_search_result_qc_precursor_query(base_url: str, headers: Dict, search_id: str) -> List[QcPrecursor]:
    response = requests.get(f"{base_url}/search_results/{search_id}/qc/precursors", headers=headers)
    response.raise_for_status()
    return [QcPrecursor.from_dict(qc) for qc in response.json()]
