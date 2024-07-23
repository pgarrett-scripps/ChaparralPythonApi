from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SearchResultDownload(BaseModel):
    """
    The search result download data.
    """
    model_config = ConfigDict(populate_by_name=True)

    config_json: str = Field(..., alias='config.json')
    matched_fragments_parquet: Optional[str] = Field(None, alias='matched_fragments.sage.parquet')
    peptide_csv: Optional[str] = Field(None, alias='peptide.csv')
    proteins_csv: Optional[str] = Field(None, alias='proteins.csv')
    results_json: Optional[str] = Field(None, alias='results.json')
    results_parquet: Optional[str] = Field(None, alias='results.sage.parquet')
