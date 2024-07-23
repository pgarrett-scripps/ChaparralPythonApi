from pydantic import BaseModel


class QcScore(BaseModel):
    """
    The quality control score data.
    """
    bin: float
    count: int
    is_decoy: bool


class QcId(BaseModel):
    """
    The identification quality control data.
    """
    filename: str
    peptides: int
    protein_groups: int
    psms: int


class QcPrecursor(BaseModel):
    """
    The precursor quality control data.
    """
    filename: str
    q10: float
    q25: float
    q50: float
    q75: float
    q90: float
