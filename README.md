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
print(api.get_projects())

# Fetch and print organization details
print(api.get_organization())

# Fetch and print all FASTA databases
print(api.get_databases())
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

- **Get All Projects:** `get_projects() -> List[Project]`
  - Retrieves a list of all projects.

- **Get Project by ID:** `get_project(project_id: str) -> Project`
  - Retrieves a specific project by its ID.

- **Create Project:** `create_project(name: str, description: str) -> Project`
  - Creates a new project.

- **Update Project:** `update_project(project_id: str, name: str, description: str, tags: List[str]) -> Project`
  - Updates an existing project.

- **Delete Project:** `delete_project(project_id: str) -> None`
  - Deletes a project by its ID.

- **Tag Projects:** `tag_projects(project_ids: List[str], tags: List[str]) -> List[Project]`
  - Adds tags to multiple projects.

- **Get Projects by Tag:** `get_projects_by_tag(tag: str) -> List[Project]`
  - Retrieves projects that have a specific tag.

#### Organization Endpoints

- **Get Organization:** `get_organization() -> Organization`
  - Retrieves the details of the organization.

- **Update Organization:** `update_organization(organization_id: str, name: str) -> Organization`
  - Updates the organization's name.

- **Invite to Organization:** `invite_to_organization(email: str) -> None`
  - Invites a new member to the organization.

- **Get Resource Usage:** `get_resource_usage() -> OrganizationUsage`
  - Retrieves the resource usage of the organization.

#### Database Endpoints

- **Get All Databases:** `get_databases() -> List[Database]`
  - Retrieves a list of all databases.

- **Get Database by ID:** `get_database(database_id: str) -> Database`
  - Retrieves a specific database by its ID.

- **Update Database:** `update_database(database_id: str, name: str, organism: str, decoy_tag: Optional[str]) -> Database`
  - Updates an existing database.

- **Create Database:** `create_database(database_bytes: bytes, filename: str) -> Database`
  - Creates a new database.

- **Delete Database:** `delete_database(database_id: str) -> None`
  - Deletes a database by its ID.

#### Search Result Endpoints

- **Get Spectra:** `get_spectra(search_result_id: str, filename: str, scannr: str) -> List[ScanData]`
  - Retrieves the spectra for a specific search result and scan number.

- **Get PSM Annotations:** `get_psm_annotations(search_result_id: str, psm_id: int) -> List[FragmentData]`
  - Retrieves the PSM annotations for a specific search result and PSM ID.

- **Get Peptide Results:** `get_peptide_results(search_result_id: str, query_id: str, query_type: Literal['peptide', 'protein'] = 'protein') -> List[PeptideResult]`
  - Retrieves the peptides for a specific search result and protein ID or peptide ID.

- **Get All Search Results:** `get_search_results() -> List[SearchResult]`
  - Retrieves a list of all search results.

- **Get Search Result by ID:** `get_search_result(search_result_id: str) -> Optional[SearchResult]`
  - Retrieves a specific search result by its ID.

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

#### User Profile Endpoints

- **Get User Profile:** `get_user_profile() -> Profile`
  - Retrieves the user's profile information.

- **Update User Profile:** `update_user_profile(first_name: str, last_name: str) -> Profile`
  - Updates the user's profile information.

#### Project File Endpoints

- **Get Project Files:** `get_project_files(project_id: str) -> List[ProjectFile]`
  - Retrieves the files for a specific project.

- **Get Project File:** `get_project_file(project_id: str, file_id: str) -> ProjectFile`
  - Retrieves a specific file from a project by its ID.

- **Upload Project File:** `upload_project_file(project_id: str, file_bytes: bytes, filename: str)`
  - Uploads a file to a specific project.

#### Search Submission Endpoints

- **Submit Search:** `submit_search(project_id: str, search_settings: Dict) -> None`
  - Submits a search request for a specific project.
