from typing import Dict
from pydantic import ValidationError, BaseModel, EmailStr
from datetime import datetime


class Profile(BaseModel):
    id: str
    email: EmailStr
    email_verified: bool
    first_name: str
    last_name: str
    agreed: bool
    created_at: datetime
    updated_at: datetime
