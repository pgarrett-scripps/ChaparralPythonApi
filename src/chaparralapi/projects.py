import requests

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Project:
    user_id: str
    organization_id: str
    id: str
    name: str
    description: Optional[str]
    tags: Optional[List[str]]
    created_at: str
    additional_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Project':
        return cls(
            user_id=d['user_id'],
            organization_id=d['organization_id'],
            id=d['id'],
            name=d['name'],
            description=d.get('description'),
            tags=d.get('tags'),
            created_at=d['created_at'],
            additional_fields={k: v for k, v in d.items() if k not in ['user_id', 'organization_id', 'id', 'name', 'description', 'tags', 'created_at']}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tags': self.tags,
            'created_at': self.created_at,
            **self.additional_fields
        }


def list_project_query(base_url: str, headers: Dict, return_json: bool = False) -> List[Project]:
    response = requests.get(f"{base_url}/projects", headers=headers)
    response.raise_for_status()
    if return_json:
        return response.json()
    return [Project.from_dict(project) for project in response.json()]


def read_project_query(base_url: str, headers: Dict, project_id: str, return_json: bool = False) -> Project:
    response = requests.get(f"{base_url}/projects/{project_id}", headers=headers)
    response.raise_for_status()
    if return_json:
        return response.json()
    return Project.from_dict(response.json())


def update_project_query(base_url: str, headers: Dict, project_id: str, data: Dict, return_json: bool = False) -> Project:
    response = requests.put(f"{base_url}/projects/{project_id}", headers=headers, json=data)
    response.raise_for_status()
    if return_json:
        return response.json()
    return Project.from_dict(response.json())


def creat_project_query(base_url: str, headers: Dict, data: Dict) -> Project:
    response = requests.post(f"{base_url}/projects", headers=headers, json=data)
    response.raise_for_status()
    if return_json:
        return response.json()
    return Project.from_dict(project_data)
