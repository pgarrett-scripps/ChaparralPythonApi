from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ProteinsGroup:
    _protein_names: str
    _descriptions: str
    _gene_names: str
    psms: int
    _peptide_sequences: str
    protein_q: float

    @property
    def protein_names(self) -> List[str]:
        return self._protein_names.split(';')

    @property
    def descriptions(self) -> List[str]:
        return self._descriptions.split(';')

    @property
    def gene_names(self) -> List[str]:
        return self._gene_names.split(';')

    @property
    def peptide_sequences(self) -> List[str]:
        return self._peptide_sequences.split(';')

    def __repr__(self) -> str:
        return f'ProteinsGroup("{self._protein_names}")'

    def dict(self):
        return {
            'protein_names': self.protein_names,
            'descriptions': self.descriptions,
            'gene_names': self.gene_names,
            'psms': self.psms,
            'peptide_sequences': self.peptide_sequences,
            'protein_q': self.protein_q
        }


@dataclass(frozen=True)
class Protein:
    name: str
    description: str
    gene_name: str
    psms: int
    _peptide_sequences: str

    @property
    def peptide_sequences(self) -> List[str]:
        return self._peptide_sequences.split(';')

    def __repr__(self) -> str:
        return f'Protein("{self.name}")'

    def dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'gene_name': self.gene_name,
            'psms': self.psms,
            'peptide_sequences': self.peptide_sequences
        }


@dataclass(frozen=True)
class Peptide:
    sequence: str
    _protein_names: str
    _descriptions: str
    _gene_names: str
    psms: int
    peptide_q: float
    best_filename: str
    best_scannr: str

    @property
    def protein_names(self) -> List[str]:
        return self._protein_names.split(';')

    @property
    def descriptions(self) -> List[str]:
        return self._descriptions.split(';')

    @property
    def gene_names(self) -> List[str]:
        return self._gene_names.split(';')

    def __repr__(self) -> str:
        return f'Peptide("{self.sequence}")'

    def dict(self):
        return {
            'sequence': self.sequence,
            'protein_names': self.protein_names,
            'descriptions': self.descriptions,
            'gene_names': self.gene_names,
            'psms': self.psms,
            'peptide_q': self.peptide_q,
            'best_filename': self.best_filename,
            'best_scannr': self.best_scannr
        }
