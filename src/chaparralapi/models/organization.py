from datetime import datetime

from pydantic import BaseModel


class Organization(BaseModel):
    """
    The organization data.
    """
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
