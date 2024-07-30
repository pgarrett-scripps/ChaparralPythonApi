
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel

from chaparralapi.models import SearchConfig


class SearchResult(BaseModel):
    """
    The search result data.
    """
    id: str
    notes: Optional[str]
    passing_psms: Optional[int]
    passing_peptides: Optional[int]
    passing_proteins: Optional[int]
    input_files: List[str]
    params: SearchConfig
    project_id: str
    project_name: str
    organization_id: str
    job_id: str
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: Literal['FAILED', 'SUCCEEDED', 'SUBMITTED', 'RUNNING', 'RUNNABLE', 'PENDING', 'STARTING']
    cpu: int
    memory: int


class PeptideResult(BaseModel):
    calcmass: float
    charge: int
    expmass: float
    filename: str
    peptide: str
    psm_id: int
    scannr: str


class FragmentData(BaseModel):
    fragment_charge: int
    fragment_intensity: float
    fragment_mz_calculated: float
    fragment_mz_experimental: float
    fragment_ordinals: int
    fragment_type: str
    psm_id: int


class ScanData(BaseModel):
    intensity: int
    isolation_lower: float
    isolation_upper: float
    level: int
    mz: float
    precursor_charge: int
    precursor_mz: float
    precursor_scan: int
    rt: float
    scan: int