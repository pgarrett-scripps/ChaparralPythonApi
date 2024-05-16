import requests

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Fasta:
    id: str
    name: str
    crc32: int
    size: int
    protein_count: int
    organism: Optional[str]
    decoy_tag: Optional[str]
    key: str
    organization_id: str
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Fasta':
        return cls(
            id=d['id'],
            name=d['name'],
            crc32=d['crc32'],
            size=d['size'],
            protein_count=d['protein_count'],
            organism=d.get('organism'),
            decoy_tag=d.get('decoy_tag'),
            key=d['key'],
            organization_id=d['organization_id'],
            additional_fields={k: v for k, v in d.items() if
                               k not in ['id', 'name', 'crc32', 'size', 'protein_count', 'organism', 'decoy_tag', 'key',
                                         'organization_id']}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'crc32': self.crc32,
            'size': self.size,
            'protein_count': self.protein_count,
            'organism': self.organism,
            'decoy_tag': self.decoy_tag,
            'key': self.key,
            'organization_id': self.organization_id,
            **self.additional_fields
        }


def list_fasta_query(base_url: str, headers: Dict, return_json: bool = False) -> List[Fasta]:
    response = requests.get(f"{base_url}/databases", headers=headers)
    response.raise_for_status()
    if return_json:
        return response.json()
    return [Fasta.from_dict(fasta) for fasta in response.json()]


def read_fasta_query(base_url: str, headers: Dict, fasta_id: str, return_json: bool = False) -> Fasta:
    response = requests.get(f"{base_url}/databases/{fasta_id}", headers=headers)
    if return_json:
        return response.json()
    return Fasta.from_dict(response.json())


# TODO: Fix this
def usePresignedFastaMutation(base_url: str, headers: Dict, data: bytes, return_json: bool = False) -> Fasta:
    response = requests.post(f"{base_url}/databases/", headers=headers, json=data)
    if return_json:
        return response.json()
    return Fasta.from_dict(response.json())


def update_fasta_query(base_url: str, headers: Dict, fasta_id: str, data: Dict, return_json: bool = False) -> Fasta:
    response = requests.put(f"{base_url}/databases/{fasta_id}", headers=headers, json=data)
    if return_json:
        return response.json()
    return Fasta.from_dict(response.json())
