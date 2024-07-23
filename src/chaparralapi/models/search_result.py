
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
    status: Literal['FAILED', 'SUCCEEDED', 'SUBMITTED', 'RUNNING', 'RUNNABLE']
    cpu: int
    memory: int
