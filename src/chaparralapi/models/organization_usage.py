from pydantic import BaseModel


class OrganizationUsage(BaseModel):
    """
    The Organization Usage data.
    """
    storage: str
    compute_cpu_s: str
    compute_mem_s: str
