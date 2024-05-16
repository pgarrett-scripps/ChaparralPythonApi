import requests

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Organization:
    id: str
    name: str
    created_at: str
    updated_at: str
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Organization':
        return cls(
            id=d['id'],
            name=d['name'],
            created_at=d['created_at'],
            updated_at=d['updated_at'],
            additional_fields={k: v for k, v in d.items() if k not in ['id', 'name', 'created_at', 'updated_at']}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            **self.additional_fields
        }


def read_organization_query(base_url: str, headers: Dict, return_json: bool = False) -> Organization:
    response = requests.get(f"{base_url}/organization", headers=headers)
    response.raise_for_status()
    if return_json:
        return response.json()
    return Organization.from_dict(response.json())


def update_organiation_query(base_url: str, headers: Dict, data: Dict, return_json: bool = False) -> Organization:
    response = requests.put(f"{base_url}/organization", headers=headers, json=data)
    response.raise_for_status()
    if return_json:
        return response.json()
    return Organization.from_dict(response.json())


def invite_organization_query(base_url: str, headers: Dict, data: Dict, return_json: bool = False) -> Dict:
    response = requests.post(f"{base_url}/organization/invite", headers=headers, json=data)
    response.raise_for_status()
    if return_json:
        return response.json()
    return response.json()
