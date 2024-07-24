from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    job_status: Optional[str]