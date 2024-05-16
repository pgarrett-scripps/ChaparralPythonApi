## Chaparral Python API

This Python package is a wrapper for the Chaparral API. It provides a simple and convenient interface for interacting with the Chaparral platform.

**Note:** Currently, it supports a limited number of API endpoints. More endpoints will be added in future releases.

## Installation

To install the package, use pip:

```bash
pip install chaparralapi
```

## Example Usage

Here's a quick example of how to use the Chaparral API client:

```python
from chaparralapi import Client

token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
api = Client(token)

# Fetch and print all projects
print(api.get_all_projects())

# Fetch and print organization details
print(api.get_organization())

# Fetch and print all FASTA databases
print(api.get_all_fastas())
```

## Obtaining the API Token

To get your Chaparral API token, follow these steps:

1. Go to the [Chaparral website](https://chaparral.ai).
2. Open the browser's developer tools (usually F12 or right-click and select "Inspect").
3. Navigate to the "Network" tab.
4. Look for a REST API call and inspect its headers.
5. Copy the token from the `Authorization` header.
6. The token will be valid for 8 hours.


## Endpoints

This section describes the endpoints available in the `Client` class for interacting with the Chaparral API.

#### Project Endpoints

- **Get All Projects:** `get_all_projects() -> List[Project]`
  - Retrieves a list of all projects.

- **Get Project by ID:** `get_project(project_id: str) -> Project`
  - Retrieves a specific project by its ID.

- **Create Project:** `create_project(name: str, description: str) -> Project`
  - Creates a new project.

- **Update Project:** `update_project(project_id: str, name: str, description: str) -> Project`
  - Updates an existing project.

- **Delete Project:** `delete_project(project_id: str) -> None`
  - Deletes a project by its ID.

#### Organization Endpoints

- **Get Organization:** `get_organization() -> Organization`
  - Retrieves the details of the organization.

- **Update Organization:** `update_organization(name: str) -> Organization`
  - Updates the organization's name.

- **Invite to Organization:** `invite_to_organization(email: str) -> None`
  - Invites a new member to the organization.

#### FASTA Endpoints

- **Get All FASTA Databases:** `get_all_fastas() -> List[Fasta]`
  - Retrieves a list of all FASTA databases.

- **Get FASTA Database by ID:** `get_fasta(fasta_id: str) -> Fasta`
  - Retrieves a specific FASTA database by its ID.

- **Update FASTA Database:** `update_fasta(fasta_id: str, name: str, organism: str, decoy_tag: Optional[str]) -> Fasta`
  - Updates an existing FASTA database.

- **Create FASTA Database:** `create_fasta() -> Fasta`
  - Creates a new FASTA database. (Not implemented)

- **Delete FASTA Database:** `delete_fasta(fasta_id: str) -> None`
  - Deletes a FASTA database by its ID.

#### Search Result Endpoints

- **Get All Search Results:** `get_all_search_results() -> List[SearchResult]`
  - Retrieves a list of all search results.

- **Get Search Result Download:** `get_search_result_download(search_result_id: str) -> SearchResultDownload`
  - Retrieves the download URLs for a specific search result.

- **Fetch Config JSON:** `fetch_config_json(search_result_id: str) -> str`
  - Fetches the config JSON file for a specific search result.

- **Fetch Matched Fragments Parquet:** `fetch_matched_fragments_parquet(search_result_id: str) -> str`
  - Fetches the matched fragments parquet file for a specific search result.

- **Fetch Peptide CSV:** `fetch_peptide_csv(search_result_id: str) -> str`
  - Fetches the peptide CSV file for a specific search result.

- **Fetch Proteins CSV:** `fetch_proteins_csv(search_result_id: str) -> str`
  - Fetches the proteins CSV file for a specific search result.

- **Fetch Results JSON:** `fetch_results_json(search_result_id: str) -> str`
  - Fetches the results JSON file for a specific search result.

- **Fetch Results Parquet:** `fetch_results_parquet(search_result_id: str) -> str`
  - Fetches the results parquet file for a specific search result.

#### QC Endpoints

- **Get QC Scores:** `get_qc_scores(search_result_id: str) -> List[QcScore]`
  - Retrieves the QC scores for a specific search result.

- **Get QC IDs:** `get_qc_ids(search_result_id: str) -> List[QcId]`
  - Retrieves the QC IDs for a specific search result.

- **Get QC Precursors:** `get_qc_precursors(search_result_id: str) -> List[QcPrecursor]`
  - Retrieves the QC precursors for a specific search result.
