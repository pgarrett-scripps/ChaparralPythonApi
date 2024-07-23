from typing import Dict, List, Optional, Any, Literal, Tuple

from .models import StaticModsConfig, VariableModsConfig, EnzymeConfig, DatabaseConfig, SearchConfig, \
    TolConfig, DesignConfig, LinearModelConfig, QuantConfig, LfqConfig, TmtConfig


def search_config_builder(database_id: str,
                          cleavage_sites: str = 'KR',
                          restrict: str = 'P',
                          cterminal: bool = True,
                          min_peptide_len: int = 7,
                          max_peptide_len: int = 50,
                          missed_cleavages: int = 2,
                          semi_enzymatic: bool = False,
                          static_mods: Optional[Dict[str, float]] = None,
                          variable_mods: Optional[Dict[str, List[float]]] = None,
                          precursor_tol_type: Literal['ppm', 'da'] = 'ppm',
                          precursor_tol: Tuple[float, float] = (-50, 50),
                          fragment_tol_type: Literal['ppm', 'da'] = 'ppm',
                          fragment_tol: Tuple[float, float] = (-10, 10),
                          isotope_errors: Tuple[int, int] = (-1, 3),
                          deisotope: bool = True,
                          chimera: bool = False,
                          wide_window: bool = False,
                          report_psms: int = 1,
                          min_peaks: int = 15,
                          max_peaks: int = 150,
                          min_matched_peaks: int = 4,
                          max_fragment_charge: int = 1,
                          predict_rt: bool = True,
                          linear_model_designs: List[Tuple[str, str, str]] = None,
                          linear_model_contrasts: List[str] = None,
                          use_lfq: bool = False,
                          lfq_ms1_ppm: int = 5,
                          lfq_spectral_angle: float = 0.7,
                          tmt: Optional[Literal['TMT6', 'TMT10', 'TMT11', 'TMT16', 'TMT18']] = None,
                          tmt_level: int = 3,
                          ) -> Dict[str, Any]:

    if static_mods is None:
        static_mods = {}

    if variable_mods is None:
        variable_mods = {}

    static_mod_config = StaticModsConfig(static_mods)
    variable_mod_config = VariableModsConfig(variable_mods)
    enzyme_config = EnzymeConfig(c_terminal=cterminal, cleave_at=cleavage_sites, max_len=max_peptide_len,
                                 min_len=min_peptide_len, missed_cleavages=missed_cleavages, restrict=restrict,
                                 semi_enzymatic=semi_enzymatic)
    database_config = DatabaseConfig(enzyme=enzyme_config, fasta=database_id, static_mods=static_mod_config,
                                     variable_mods=variable_mod_config)
    precursor_tolerance = TolConfig(**{precursor_tol_type: list(precursor_tol)})
    fragment_tolerance = TolConfig(**{fragment_tol_type: list(fragment_tol)})

    linear_model_config = LinearModelConfig(contrasts=[], designs=[])
    if linear_model_designs is not None:
        linear_model_config.contrasts = linear_model_contrasts
    if linear_model_designs is not None:
        linear_model_config.designs = [DesignConfig(filename=filename, group=group, tmt_channel=tmt_channel) for
                                       filename, group, tmt_channel in linear_model_designs]

    quant_config = QuantConfig(lfq=use_lfq,
                               lfq_settings=LfqConfig(ppm_tolerance=lfq_ms1_ppm,
                                                      spectral_angle=lfq_spectral_angle),
                               tmt=tmt,
                               tmt_settings=TmtConfig(level=tmt_level))

    search_config = SearchConfig(chimera=chimera, database=database_config, deisotope=deisotope,
                                 fragment_tol=fragment_tolerance,
                                 isotope_errors=list(isotope_errors), linear_model=linear_model_config,
                                 max_fragment_charge=max_fragment_charge,
                                 max_peaks=max_peaks, min_matched_peaks=min_matched_peaks, min_peaks=min_peaks,
                                 precursor_tol=precursor_tolerance, predict_rt=predict_rt, quant=quant_config,
                                 report_psms=report_psms,
                                 wide_window=wide_window)

    return search_config.to_post_data()
