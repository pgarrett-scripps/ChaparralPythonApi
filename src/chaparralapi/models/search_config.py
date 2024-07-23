from typing import Optional, List, Dict, Any

from pydantic import BaseModel, field_validator, RootModel, root_validator, model_validator

VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY^$[]")


class StaticModsConfig(RootModel[Dict[str, float]]):
    @field_validator('root')
    @classmethod
    def check_valid_amino_acids(cls, v: Dict[str, float]) -> Dict[str, float]:
        for key in v.keys():
            if key not in VALID_AMINO_ACIDS:
                raise ValueError(f"{key} is not a valid amino acid or special modification character")
        return v


class VariableModsConfig(RootModel[Dict[str, List[float]]]):
    @field_validator('root')
    @classmethod
    def check_valid_amino_acids(cls, v: Dict[str, List[float]]) -> Dict[str, List[float]]:
        for key in v.keys():
            if key not in VALID_AMINO_ACIDS:
                raise ValueError(f"{key} is not a valid amino acid or special modification character")
        return v


class EnzymeConfig(BaseModel):
    c_terminal: bool
    cleave_at: str
    max_len: int
    min_len: int
    missed_cleavages: int
    restrict: Optional[Any] = None
    semi_enzymatic: Optional[bool] = None


class DatabaseConfig(BaseModel):
    bucket_size: Optional[Any] = None
    decoy_tag: Optional[Any] = None
    enzyme: EnzymeConfig
    fasta: str
    fragment_max_mz: Optional[Any] = None
    fragment_min_mz: Optional[Any] = None
    generate_decoys: Optional[Any] = None
    ion_kinds: Optional[Any] = None
    max_variable_mods: Optional[Any] = None
    min_ion_index: Optional[Any] = None
    peptide_max_mass: Optional[Any] = None
    peptide_min_mass: Optional[Any] = None
    static_mods: StaticModsConfig
    variable_mods: VariableModsConfig


class DesignConfig(BaseModel):
    filename: str
    group: str
    tmt_channel: Optional[Any] = None


class LinearModelConfig(BaseModel):
    contrasts: List[Any]
    designs: List[DesignConfig]


class TolConfig(BaseModel):
    ppm: Optional[List[int]] = None
    da: Optional[List[int]] = None

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_filled_and_order(cls, values):
        ppm, da = values.get('ppm'), values.get('da')

        if ppm is None and da is None:
            raise ValueError('At least one of "ppm" or "da" must be provided.')

        if ppm:
            if len(ppm) != 2:
                raise ValueError('"ppm" must contain exactly 2 values.')
            if ppm[0] >= ppm[1]:
                raise ValueError('In "ppm", the first value must be smaller than the second.')

        if da:
            if len(da) != 2:
                raise ValueError('"da" must contain exactly 2 values.')
            if da[0] >= da[1]:
                raise ValueError('In "da", the first value must be smaller than the second.')

        return values


class LfqConfig(BaseModel):
    ppm_tolerance: Optional[int] = None
    da_tolerance: Optional[int] = None
    spectral_angle: Optional[float] = None  # In post request but not in returned data
    combine_charge_states: Optional[bool] = None  # in post request but not in returned data

    @model_validator(mode='before')
    @classmethod
    def check_at_least_one_filled(cls, values):
        ppm, da = values.get('ppm_tolerance'), values.get('da_tolerance')

        if ppm is None and da is None:
            raise ValueError('At least one of "ppm_tolerance" or "da_tolerance" must be provided.')

        return values


class TmtConfig(BaseModel):
    level: int


class QuantConfig(BaseModel):
    lfq: bool
    lfq_settings: LfqConfig
    tmt: Optional[Any] = None
    tmt_settings: Optional[TmtConfig] = None


class SearchConfig(BaseModel):
    chimera: bool
    database: DatabaseConfig
    deisotope: bool
    fragment_tol: TolConfig
    isotope_errors: List[int]
    linear_model: LinearModelConfig
    max_fragment_charge: int
    max_peaks: int
    min_matched_peaks: int
    min_peaks: int
    precursor_tol: TolConfig
    predict_rt: bool
    quant: QuantConfig
    report_psms: int
    wide_window: bool

    @model_validator(mode='before')
    @classmethod
    def check_isotope_errors(cls, values):
        if len(values['isotope_errors']) != 2:
            raise ValueError('isotope_errors must contain exactly 2 values')
        if values['isotope_errors'][0] >= values['isotope_errors'][1]:
            raise ValueError('isotope_errors must be in increasing order')
        return values

    def to_post_data(self):
        data = self.dict()

        def remove_none_values(d):
            """
            Recursively removes keys with None values from a dictionary and its sub-dictionaries.
            :param d: The dictionary to process.
            :return: The cleaned dictionary.
            """
            if not isinstance(d, dict):
                return d
            return {k: remove_none_values(v) for k, v in d.items() if v is not None}


        return remove_none_values(data)
