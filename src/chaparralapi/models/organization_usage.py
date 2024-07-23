from pydantic import BaseModel


class OrganizationUsage(BaseModel):
    storage: str
    compute_cpu_s: str
    compute_mem_s: str
