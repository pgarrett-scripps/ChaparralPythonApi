from typing import Optional, Dict, Any

import requests
from requests import Timeout


def get_headers(token: str) -> Dict[str, str]:
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


def get(token: str, url: str, timeout: Optional[int] = None) -> Any:
    try:
        response = requests.get(url=url,
                                headers=get_headers(token),
                                timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc


def post(token: str, url: str, data: Dict[str, Any], timeout: Optional[int] = None) -> Optional[Any]:
    try:
        response = requests.post(url=url,
                                 headers=get_headers(token),
                                 json=data,
                                 timeout=timeout)
        response.raise_for_status()
        if response.text:
            return response.json()
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc


def put(token: str, url: str, data: Dict[str, Any], timeout: Optional[int] = None) -> Any:
    try:
        response = requests.put(url=url,
                                headers=get_headers(token),
                                json=data,
                                timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc


def delete(token: str, url: str, timeout: Optional[int] = None) -> None:
    try:
        response = requests.delete(url=url,
                                   headers=get_headers(token),
                                   timeout=timeout)
        response.raise_for_status()
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc

