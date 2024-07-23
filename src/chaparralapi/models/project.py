from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Project(BaseModel):
    """
    The project data.
    """
    user_id: str
    organization_id: str
    id: str
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime
    