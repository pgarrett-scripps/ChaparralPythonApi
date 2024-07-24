from typing import Dict
from pydantic import ValidationError, BaseModel, EmailStr
from datetime import datetime


class Profile(BaseModel):
    """
    The User Profile data.
    """
    id: str
    email: EmailStr
    email_verified: bool
    first_name: str
    last_name: str
    agreed: bool
    created_at: datetime
    updated_at: datetime
