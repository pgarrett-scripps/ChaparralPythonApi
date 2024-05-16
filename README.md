## Chaparral Python API

1) This python package is a wrapper for the Chaparral API. It provides a simple interface to interact with the Chaparral API.
2) Currently, it only supports a limited number of API endpoints. More will be added in the future.

## Install 

```bash
pip install chaparralapi
```

## Example Usage
```python
token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
api = MyApi(token)
print(api.list_projects())
print(api.list_fasta())
print(api.read_organization())
```

## Where to get the token?
1) Go to the Chaparral website
2) click on inspect webpage
3) Go to the network tab
4) look for a rest api call
5) copy the token from the headers
6) The token will be valid for 8 hours
