from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel

from ..custom_types import STATUS_TYPES


class ProjectFile(BaseModel):
    """
    The Project File data. (.Raw and .D folders)
    """
    id: str
    file: str
    extension: str
    crc32: int
    size: int
    project_id: str
    organization_id: str
    created_at: datetime
    job_id: Optional[str]
    job_status: Optional[STATUS_TYPES] = None