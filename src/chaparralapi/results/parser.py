import csv
from typing import Generator, List

from .dclasses import Peptide,ProteinsGroup,Protein


def parse_peptides(text: str) -> Generator[Peptide, None, None]:
    reader = csv.reader(text.splitlines()[1:])
    for row in reader:
        peptide, proteins, descriptions, gene_names, psms, peptide_q, best_filename, best_scannr = row
        yield Peptide(peptide.strip(), proteins.strip(), descriptions.strip(), gene_names.strip(), int(psms),
                      float(peptide_q),
                      best_filename.strip(), best_scannr.strip())


def parse_protein_groups(text: str) -> Generator[ProteinsGroup, None, None]:
    reader = csv.reader(text.splitlines()[1:])
    for row in reader:
        proteins, descriptions, gene_names, psms, peptides, protein_q = row
        yield ProteinsGroup(proteins.strip(), descriptions.strip(), gene_names.strip(), int(psms.strip()),
                            peptides.strip(), float(protein_q.strip()))


def parse_proteins(peptides: List[Peptide]) -> List[Protein]:
    for peptide in peptides:
        for protein, description, gene_name in zip(peptide.protein_names, peptide.descriptions, peptide.gene_names):
            yield Protein(protein, description, gene_name, peptide.psms, peptide.sequence)
