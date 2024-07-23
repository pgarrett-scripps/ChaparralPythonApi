from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectFile(BaseModel):
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