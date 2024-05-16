from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Project(BaseModel):
    user_id: str
    organization_id: str
    id: str
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime


class Organization(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class Fasta(BaseModel):
    id: str
    name: str
    crc32: int
    size: int
    protein_count: int
    organism: Optional[str] = None
    decoy_tag: Optional[str] = None
    key: str
    organization_id: str


class SearchResult(BaseModel):
    id: str
    notes: Optional[str] = None
    passing_psms: Optional[int] = None
    passing_peptides: Optional[int] = None
    passing_proteins: Optional[int] = None
    input_files: List[str]
    params: Dict[str, Any]
    project_id: str
    project_name: str
    organization_id: str
    job_id: str
    created_at: datetime
    started_at: datetime
    finished_at: datetime
    status: str
    cpu: int
    memory: int


class SearchResultDownload(BaseModel):
    config_json: str = Field(..., alias='config.json')
    matched_fragments_parquet: str = Field(..., alias='matched_fragments.sage.parquet')
    peptide_csv: str = Field(..., alias='peptide.csv')
    proteins_csv: str = Field(..., alias='proteins.csv')
    results_json: str = Field(..., alias='results.json')
    results_parquet: str = Field(..., alias='results.sage.parquet')

    class Config:
        populate_by_name = True


class QcScore(BaseModel):
    bin: float
    count: int
    is_decoy: bool


class QcId(BaseModel):
    filename: str
    peptides: int
    protein_groups: int
    psms: int


class QcPrecursor(BaseModel):
    filename: str
    q10: float
    q25: float
    q50: float
    q75: float
    q90: float
