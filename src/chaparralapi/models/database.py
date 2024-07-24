from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Database(BaseModel):
    """
    The Database data.
    """
    id: str
    name: str
    crc32: int
    size: int
    protein_count: int
    organism: Optional[str]
    decoy_tag: Optional[str]
    key: str
    organization_id: str
