from functools import cached_property
from typing import Dict, Set
from typing import List, Generator

from .dclasses import Protein, ProteinsGroup, Peptide
from .parser import parse_protein_groups, parse_proteins, parse_peptides
from .. import models, Client


class ProteinGroupIterable:

    def __init__(self, protein_group: ProteinsGroup, res: 'Result') -> None:
        self.protein_group = protein_group
        self.res = res

    def proteins(self) -> Generator['ProteinIterable', None, None]:
        for protein in self.res.group_to_protein[self.protein_group]:
            yield ProteinIterable(protein, self.res)

    def peptides(self) -> Generator['PeptideIterable', None, None]:
        for peptide in self.res.group_to_peptide[self.protein_group]:
            yield PeptideIterable(peptide, self.res)

    def psms(self) -> Generator['PsmIterable', None, None]:
        """
        Uses API so will be slow
        """
        for peptide_iterable in self.peptides():
            for psm in peptide_iterable.psms():
                yield psm

    def __repr__(self) -> str:
        return f'ProteinGroupIterable("{self.protein_group._protein_names}")'


class ProteinIterable:

    def __init__(self, protein: Protein, res: 'Result') -> None:
        self.protein = protein
        self.res = res

    def protein_groups(self) -> Generator['ProteinGroupIterable', None, None]:
        for group in self.res.protein_to_group[self.protein]:
            yield ProteinGroupIterable(group, self.res)

    def peptides(self) -> Generator['PeptideIterable', None, None]:
        for peptide in self.res.protein_to_peptides[self.protein]:
            yield PeptideIterable(peptide, self.res)

    def psms(self) -> Generator['PsmIterable', None, None]:
        """
        Uses API so will be slow
        """
        for peptide_iterable in self.peptides():
            for psm in peptide_iterable.psms():
                yield psm

    def __repr__(self) -> str:
        return f'ProteinIterable("{self.protein.name}")'


class PeptideIterable:

    def __init__(self, peptide: Peptide, res: 'Result') -> None:
        self.peptide = peptide
        self.res = res

    def protein_groups(self) -> Generator['ProteinGroupIterable', None, None]:
        for group in self.res.peptide_to_groups[self.peptide]:
            yield ProteinGroupIterable(group, self.res)

    def proteins(self) -> Generator['ProteinIterable', None, None]:
        for protein in self.res.peptide_to_proteins[self.peptide]:
            yield ProteinIterable(protein, self.res)

    def psms(self) -> Generator['PsmIterable', None, None]:
        """
        Uses API so will be slow
        """
        for psm in self.res.client.get_peptide_results(self.res.search_id, self.peptide.sequence, 'peptide'):
            yield PsmIterable(psm, self.res)

    def __repr__(self) -> str:
        return f'PeptideIterable("{self.peptide.sequence}")'


class PsmIterable:

    def __init__(self, psm: models.PeptideResult, res: 'Result') -> None:
        self.psm = psm
        self.res = res

    def protein_groups(self) -> Generator['ProteinGroupIterable', None, None]:
        peptide = self.res.peptide_sequence_to_peptide[self.psm.peptide]
        for group in self.res.peptide_to_groups[peptide]:
            yield ProteinGroupIterable(group, self.res)

    def proteins(self) -> Generator['ProteinIterable', None, None]:
        peptide = self.res.peptide_sequence_to_peptide[self.psm.peptide]
        for protein in self.res.peptide_to_proteins[peptide]:
            yield ProteinIterable(protein, self.res)

    def peptides(self) -> Generator['PeptideIterable', None, None]:
        yield PeptideIterable(self.res.peptide_sequence_to_peptide[self.psm.peptide], self.res)

    def spectra(self) -> List[models.ScanData]:
        """
        Uses API so will be slow
        """
        return self.res.client.get_spectra(self.res.search_id, self.psm.filename, self.psm.scannr)

    def annotations(self) -> List[models.FragmentData]:
        """
        Uses API so will be slow
        """
        return self.res.client.get_psm_annotations(self.res.search_id, self.psm.psm_id)

    def __repr__(self) -> str:
        return f'PsmIterable("{self.psm.peptide}", {self.psm.psm_id})'


class Result:

    def __init__(self, client: Client, search_id: str) -> None:
        self.client = client
        self.search_id = search_id

        self.proteins: List[Protein] = []
        self.peptides: List[Peptide] = []
        self.protein_groups: List[ProteinsGroup] = []

        self.group_to_protein: Dict[ProteinsGroup, Set[Protein]] = {}
        self.protein_to_group: Dict[Protein, Set[ProteinsGroup]] = {}

        self.group_to_peptide: Dict[ProteinsGroup, Set[Peptide]] = {}
        self.peptide_to_groups: Dict[Peptide, Set[ProteinsGroup]] = {}

        self.protein_to_peptides: Dict[Protein, Set[Peptide]] = {}
        self.peptide_to_proteins: Dict[Peptide, Set[Protein]] = {}

        self.setup_peptides()
        self.setup_proteins()
        self.setup_maps()

        self.peptide_sequence_to_peptide: Dict[str, Peptide] = {}
        for peptide in self.peptides:
            self.peptide_sequence_to_peptide[peptide.sequence] = peptide

    def setup_maps(self):
        for protein_group in self.protein_groups:
            proteins_in_group = set()
            for protein_sequence in protein_group.protein_names:
                protein = next(protein for protein in self.proteins if protein.name == protein_sequence)
                proteins_in_group.add(protein)

            peptides_in_group = set()
            for peptide_sequence in protein_group.peptide_sequences:
                peptide = next(peptide for peptide in self.peptides if peptide.sequence == peptide_sequence)
                peptides_in_group.add(peptide)

            self.group_to_protein[protein_group] = proteins_in_group
            self.group_to_peptide[protein_group] = peptides_in_group

        # reverse mapping
        for protein_group, proteins in self.group_to_protein.items():
            for protein in proteins:
                self.protein_to_group.setdefault(protein, set()).add(protein_group)

        for protein_group, peptides in self.group_to_peptide.items():
            for peptide in peptides:
                self.peptide_to_groups.setdefault(peptide, set()).add(protein_group)

        for peptide in self.peptides:
            proteins = set()
            for protein_name in peptide.protein_names:
                protein = next(protein for protein in self.proteins if protein.name == protein_name)
                proteins.add(protein)
            self.peptide_to_proteins[peptide] = proteins

        # reverse mapping
        for peptide, proteins in self.peptide_to_proteins.items():
            for protein in proteins:
                self.protein_to_peptides.setdefault(protein, set()).add(peptide)

    def setup_proteins(self):
        data = self.client.fetch_proteins_csv(self.search_id).decode()
        self.protein_groups = list(parse_protein_groups(data))
        uncombined_proteins = list(parse_proteins(self.peptides))

        # Sort by name
        uncombined_proteins = sorted(uncombined_proteins, key=lambda x: x.name)
        merged_proteins = []
        curr_protein = None
        psm_cnt = 0
        peptides = []

        for uncombined_protein in uncombined_proteins:
            if curr_protein is None or curr_protein.name != uncombined_protein.name:
                if curr_protein is not None:
                    merged_proteins.append(
                        Protein(curr_protein.name, curr_protein.description, curr_protein.gene_name, psm_cnt,
                                ';'.join(peptides))
                    )

                curr_protein = uncombined_protein
                psm_cnt = 0
                peptides = []

            psm_cnt += uncombined_protein.psms
            peptides.append(uncombined_protein.peptide_sequences[0])  # Assuming there is only 1 peptide sequence

        if curr_protein is not None:
            merged_proteins.append(
                Protein(curr_protein.name, curr_protein.description, curr_protein.gene_name, psm_cnt,
                        ';'.join(peptides))
            )

        self.proteins = merged_proteins

    def setup_peptides(self):
        data = self.client.fetch_peptide_csv(self.search_id).decode()
        self.peptides = list(parse_peptides(data))

    @cached_property
    def info(self) -> models.SearchResult:
        return self.client.get_search_result(self.search_id)

    def protein_group_iterable(self) -> Generator[ProteinGroupIterable, None, None]:
        for group in self.protein_groups:
            yield ProteinGroupIterable(group, self)

    def protein_iterable(self) -> Generator[ProteinIterable, None, None]:
        for protein in self.proteins:
            yield ProteinIterable(protein, self)

    def peptide_iterable(self) -> Generator[PeptideIterable, None, None]:
        for peptide in self.peptides:
            yield PeptideIterable(peptide, self)

    def get_protein_iterable(self, name: str) -> ProteinIterable:
        protein = next(protein for protein in self.proteins if protein.name == name)
        return ProteinIterable(protein, self)

    def get_protein_group_iterable(self, name: str) -> ProteinGroupIterable:
        group = next(group for group in self.protein_groups if name in group.protein_names)
        return ProteinGroupIterable(group, self)

    def get_peptide_iterable(self, sequence: str) -> PeptideIterable:
        peptide = next(peptide for peptide in self.peptides if peptide.sequence == sequence)
        return PeptideIterable(peptide, self)
