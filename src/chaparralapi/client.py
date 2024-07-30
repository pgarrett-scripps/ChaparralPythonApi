"""
The Client class is a wrapper around the Chaparral API.
"""
import os
from typing import List, Optional, Dict, IO, TextIO, BinaryIO, Literal
import logging

import requests
from requests import HTTPError
from requests.exceptions import Timeout

from .constants import DEFAULT_BASE_URL
from . import models
from . import routes
from .utils import get_best_chaparral_server

LOGGING_LEVELS = Literal['CRITICAL', 'FATAL', 'ERROR', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']

def _fetch_file(url: str, timeout: Optional[int]) -> bytes:
    """
    Fetches the content of a file from a given URL.

    :param url: The URL of the file to fetch.
    :type url: str
    :param timeout: The timeout duration for the request in seconds.
    :type timeout: Optional[int]
    :return: The content of the file in bytes.
    :rtype: bytes
    :raises Timeout: If the request times out.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.content
    except Timeout as exc:
        raise Timeout(f'Request to {url} timed out.') from exc


class Client:
    """
    The Client class is a wrapper around the Chaparral API.

    :param token: The Chaparral API token.
    :type token: str
    :param base_url: The Chaparral API base URL. Defaults to DEFAULT_BASE_URL.
    :type base_url: str | None
    :param timeout: The request timeout in seconds. Defaults to 10 seconds.
    :type timeout: float | None
    :param file_upload_timeout: The timeout duration for file uploads in seconds. Defaults to 60 seconds.
    :type file_upload_timeout: float | None
    """

    def __init__(self, token: str, base_url: Optional[str] = DEFAULT_BASE_URL, timeout: Optional[float] = 10,
                 file_upload_timeout: Optional[float] = 60, log_level: LOGGING_LEVELS = 'INFO'):
        self.token = token

        if base_url is None:
            base_url = get_best_chaparral_server()

        self.base_url = base_url
        self.timeout = timeout
        self.file_upload_timeout = file_upload_timeout

        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def configure_logging(self, log_level: LOGGING_LEVELS):
        """
        Configures the logging level.

        :param log_level: The logging level to set.
        :type log_level: str
        """
        self.logger.setLevel(log_level)

    def test_connection(self) -> bool:
        """
        Tests the connection to the Chaparral API.

        :return: True if the connection is successful, False otherwise.
        """
        try:
            self.get_user_profile()
            return True
        except HTTPError:
            return False

    def get_projects(self) -> List[models.Project]:
        """
        Retrieves a list of projects.

        :return: A list of Project models.
        :rtype: List[models.Project]
        """
        projects_data = routes.project.get_projects(token=self.token, base_url=self.base_url, timeout=self.timeout)
        self.logger.debug(f'Projects data retrieved: {projects_data}')
        return [models.Project.model_validate(project) for project in projects_data]

    def get_project(self, project_id: str) -> models.Project:
        """
        Retrieves a specific project by its ID.

        :param project_id: The ID of the project to retrieve.
        :type project_id: str
        :return: The Project model.
        :rtype: models.Project
        """
        project_data = routes.project.get_project(token=self.token, project_id=project_id, base_url=self.base_url,
                                                  timeout=self.timeout)
        self.logger.debug(f'Project data retrieved: {project_data}')
        return models.Project.model_validate(project_data)

    def get_projects_by_tag(self, tag: str) -> List[models.Project]:
        """
        Retrieves projects that have a specific tag.

        :param tag: The tag to filter projects by.
        :type tag: str
        :return: A list of Project models that have the specified tag.
        :rtype: List[models.Project]
        """
        projects = self.get_projects()
        return [project for project in projects if project.tags and tag in project.tags]

    def create_project(self, name: str, description: str) -> models.Project:
        """
        Creates a new project.

        :param name: The name of the new project.
        :type name: str
        :param description: The description of the new project.
        :type description: str
        :return: The created Project model.
        :rtype: models.Project
        """
        data = {'name': name, 'description': description}
        project_data = routes.project.create_project(token=self.token, data=data, base_url=self.base_url,
                                                     timeout=self.timeout)
        return models.Project.model_validate(project_data)

    def update_project(self, project_id: str, name: str, description: str, tags: List[str]) -> models.Project:
        """
        Updates an existing project.

        :param project_id: The ID of the project to update.
        :type project_id: str
        :param name: The new name of the project.
        :type name: str
        :param description: The new description of the project.
        :type description: str
        :param tags: The new tags for the project.
        :type tags: List[str]
        :return: The updated Project model.
        :rtype: models.Project
        """
        data = {'name': name, 'description': description, 'tags': tags}
        updated_data = routes.project.update_project(token=self.token, project_id=project_id, data=data,
                                                     base_url=self.base_url, timeout=self.timeout)
        return models.Project.model_validate(updated_data)

    def tag_projects(self, project_ids: List[str], tags: List[str]) -> List[models.Project]:
        """
        Adds tags to multiple projects.

        :param project_ids: A list of project IDs to tag.
        :type project_ids: List[str]
        :param tags: A list of tags to add to the projects.
        :type tags: List[str]
        :return: A list of updated Project models.
        :rtype: List[models.Project]
        """
        projects = []
        for project in [self.get_project(project_id) for project_id in project_ids]:
            project.tags = tags
            if project.tags is None:
                project.tags = []
            updated_project = self.update_project(project.id, project.name, project.description, project.tags + tags)
            projects.append(updated_project)
        return projects

    def delete_project(self, project_id: str) -> None:
        """
        Deletes a project.

        :param project_id: The ID of the project to delete.
        :type project_id: str
        """
        routes.project.delete_project(token=self.token, project_id=project_id, base_url=self.base_url,
                                      timeout=self.timeout)

    def get_organization(self) -> models.Organization:
        """
        Retrieves the organization information.

        :return: The Organization model.
        :rtype: models.Organization
        """
        organization_data = routes.organization.get_organization(token=self.token, base_url=self.base_url,
                                                                 timeout=self.timeout)
        return models.Organization.model_validate(organization_data)

    def update_organization(self, organization_id: str, name: str) -> models.Organization:
        """
        Updates the organization information.

        :param organization_id: The ID of the organization to update.
        :type organization_id: str
        :param name: The new name of the organization.
        :type name: str
        :return: The updated Organization model.
        :rtype: models.Organization
        """
        data = {'name': name}
        updated_data = routes.organization.update_organization(token=self.token, organization_id=organization_id,
                                                               data=data, base_url=self.base_url, timeout=self.timeout)
        return models.Organization.model_validate(updated_data)

    def invite_to_organization(self, email: str) -> None:
        """
        Sends an invitation to join the organization.

        :param email: The email address to send the invitation to.
        :type email: str
        """
        routes.organization_invite.create_organization_invite(token=self.token, data={'email': email},
                                                              base_url=self.base_url, timeout=self.timeout)

    def get_databases(self) -> List[models.Database]:
        """
        Retrieves a list of databases.

        :return: A list of Database models.
        :rtype: List[models.Database]
        """
        datas = routes.databases.get_databases(token=self.token, base_url=self.base_url, timeout=self.timeout)
        return [models.Database.model_validate(data) for data in datas]

    def get_database(self, database_id: str) -> models.Database:
        """
        Retrieves a specific database by its ID.

        :param database_id: The ID of the database to retrieve.
        :type database_id: str
        :return: The Database model.
        :rtype: models.Database
        """
        data = routes.databases.get_database(token=self.token, database_id=database_id, base_url=self.base_url,
                                             timeout=self.timeout)
        return models.Database.model_validate(data)

    def update_database(self, database_id: str, name: str, organism: str, decoy_tag: Optional[str]) -> models.Database:
        """
        Updates a database.

        :param database_id: The ID of the database to update.
        :type database_id: str
        :param name: The new name of the database.
        :type name: str
        :param organism: The organism of the database.
        :type organism: str
        :param decoy_tag: The decoy tag for the database. Optional.
        :type decoy_tag: Optional[str]
        :return: The updated Database model.
        :rtype: models.Database
        """
        data = {'name': name, 'organism': organism, 'decoy_tag': decoy_tag}
        updated_data = routes.databases.update_database(token=self.token, database_id=database_id, data=data,
                                                        base_url=self.base_url, timeout=self.timeout)
        return models.Database.model_validate(updated_data)

    def create_database(self, database_bytes: bytes, filename: str) -> models.Database:
        """
        Creates a new database.

        :param database_bytes: The bytes of the database file.
        :type database_bytes: bytes
        :param filename: The name of the database file.
        :type filename: str
        :return: The created Database model.
        :rtype: models.Database
        """
        created_data = routes.databases.create_database(token=self.token, database_bytes=database_bytes,
                                                        filename=filename,
                                                        base_url=self.base_url, timeout=self.timeout)
        return models.Database.model_validate(created_data)

    def delete_database(self, database_id: str) -> None:
        """
        Deletes a database.

        :param database_id: The ID of the database to delete.
        :type database_id: str
        """
        routes.databases.delete_database(token=self.token, database_id=database_id, base_url=self.base_url,
                                         timeout=self.timeout)

    def get_search_results(self) -> List[models.SearchResult]:
        """
        Retrieves a list of search results.

        :return: A list of SearchResult models.
        :rtype: List[models.SearchResult]
        """
        results_data = routes.search_results.get_search_results(token=self.token, base_url=self.base_url,
                                                                timeout=self.timeout)
        return [models.SearchResult.model_validate(result) for result in results_data]

    def get_search_result(self, search_result_id: str) -> Optional[models.SearchResult]:
        """
        Retrieves a specific search result by its ID.

        :param search_result_id: The ID of the search result to retrieve.
        :type search_result_id: str
        :return: The SearchResult model or None if not found.
        :rtype: Optional[models.SearchResult]
        """
        search_results = self.get_search_results()
        return next((result for result in search_results if result.id == search_result_id), None)

    def get_search_result_download(self, search_result_id: str) -> models.SearchResultDownload:
        """
        Retrieves the search result download information by its ID.

        :param search_result_id: The ID of the search result download to retrieve.
        :type search_result_id: str
        :return: The SearchResultDownload model.
        :rtype: models.SearchResultDownload
        """
        result_download_data = (
            routes.search_results_download.read_search_result_download(token=self.token,
                                                                       search_result_id=search_result_id,
                                                                       base_url=self.base_url,
                                                                       timeout=self.timeout))
        return models.SearchResultDownload.model_validate(result_download_data)

    def fetch_config_json(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the configuration JSON file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the configuration JSON file or None if download_path is provided.
        :rtype: str | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        config_json = _fetch_file(search_result_download.config_json, self.timeout)

        if download_path:
            with open(download_path, 'wb') as f:
                f.write(config_json)
        else:
            return config_json

    def fetch_matched_fragments_parquet(self, search_result_id: str, download_path: Optional[str] = None) \
            -> Optional[bytes]:
        """
        Fetches the matched fragments Parquet file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the matched fragments Parquet file or None if download_path is provided.
        :rtype: bytes | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        matched_fragments_parquet = _fetch_file(search_result_download.matched_fragments_parquet, self.timeout)
        if download_path:
            with open(download_path, 'wb') as f:
                f.write(matched_fragments_parquet)
        else:
            return matched_fragments_parquet

    def fetch_peptide_csv(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the peptide CSV file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the peptide CSV file. or None if download_path is provided.
        :rtype: bytes | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        peptide_csv = _fetch_file(search_result_download.peptide_csv, self.timeout)
        if download_path:
            with open(download_path, 'wb') as f:
                f.write(peptide_csv)
        else:
            return peptide_csv

    def fetch_proteins_csv(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the proteins CSV file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the proteins CSV file or None if download_path is provided.
        :rtype: bytes | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        proteins_csv = _fetch_file(search_result_download.proteins_csv, self.timeout)
        if download_path:
            with open(download_path, 'wb') as f:
                f.write(proteins_csv)
        else:
            return proteins_csv

    def fetch_results_json(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the results JSON file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the results JSON file or None if download_path is provided.
        :rtype: bytes | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        results_json = _fetch_file(search_result_download.results_json, self.timeout)
        if download_path:
            with open(download_path, 'wb') as f:
                f.write(results_json)
        else:
            return results_json

    def fetch_results_parquet(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the results Parquet file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the results Parquet file or None if download_path is provided.
        :rtype: bytes | None
        """
        search_result_download = self.get_search_result_download(search_result_id)
        results_parquet = _fetch_file(search_result_download.results_parquet, self.timeout)

        if download_path:
            with open(download_path, 'wb') as f:
                f.write(results_parquet)
        else:
            return results_parquet

    def download_all_files(self, search_result_id: str, download_folder: str, folder_name: Optional[str] = None):
        """
        Downloads all the files for a specific search result to a specified folder.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_folder: The folder to save the downloaded files.
        :type download_folder: str
        :param folder_name: The name of the folder to save the files. Optional, defaults to the search result ID.
        :type folder_name: str | None
        """

        if folder_name is None:
            folder_name = search_result_id

        download_path = os.path.join(download_folder, folder_name)
        os.makedirs(download_path, exist_ok=True)

        # Define the file types and corresponding methods
        file_types = {
            "config.json": self.fetch_config_json,
            "matched_fragments.parquet": self.fetch_matched_fragments_parquet,
            "peptide.csv": self.fetch_peptide_csv,
            "proteins.csv": self.fetch_proteins_csv,
            "results.json": self.fetch_results_json,
            "results.parquet": self.fetch_results_parquet,
        }

        for filename, fetch_method in file_types.items():
            fetch_method(search_result_id=search_result_id, download_path=os.path.join(download_path, filename))

    def get_qc_scores(self, search_result_id: str) -> List[models.QcScore]:
        """
        Retrieves the QC scores for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcScore models.
        :rtype: List[models.QcScore]
        """
        qc_scores_data = routes.search_result_qc.get_qc_scores(token=self.token, search_result_id=search_result_id,
                                                               base_url=self.base_url, timeout=self.timeout)
        return [models.QcScore.model_validate(score) for score in qc_scores_data]

    def get_qc_ids(self, search_result_id: str) -> List[models.QcId]:
        """
        Retrieves the QC IDs for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcId models.
        :rtype: List[models.QcId]
        """
        qc_ids_data = routes.search_result_qc.get_qc_ids(token=self.token, search_result_id=search_result_id,
                                                         base_url=self.base_url, timeout=self.timeout)
        return [models.QcId.model_validate(qc_id) for qc_id in qc_ids_data]

    def get_qc_precursors(self, search_result_id: str) -> List[models.QcPrecursor]:
        """
        Retrieves the QC precursors for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcPrecursor models.
        :rtype: List[models.QcPrecursor]
        """
        qc_precursors_data = routes.search_result_qc.get_qc_precursors(token=self.token,
                                                                       search_result_id=search_result_id,
                                                                       base_url=self.base_url, timeout=self.timeout)
        return [models.QcPrecursor.model_validate(precursor) for precursor in qc_precursors_data]

    def get_project_files(self, project_id: str) -> List[models.ProjectFile]:
        """
        Retrieves the files for a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: A list of ProjectFile models.
        :rtype: List[models.ProjectFile]
        """
        project_files_data = routes.project_file.get_project_files(token=self.token, project_id=project_id,
                                                                   base_url=self.base_url, timeout=self.timeout)
        return [models.ProjectFile.model_validate(file) for file in project_files_data]

    def get_project_file(self, project_id: str, file_id: str) -> models.ProjectFile:
        """
        Retrieves a specific file from a project by its ID.

        :param project_id: The ID of the project.
        :type project_id: str
        :param file_id: The ID of the file to retrieve.
        :type file_id: str
        :return: The ProjectFile model.
        :rtype: models.ProjectFile
        """
        raw_files = self.get_project_files(project_id)
        return next((raw_file for raw_file in raw_files if raw_file.id == file_id), None)

    def upload_project_file(self, project_id: str, file: IO, filename: str) -> None:
        """
        Uploads a file to a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param file_bytes: The bytes of the file to upload.
        :type file_bytes: bytes
        :param filename: The name of the file to upload.
        :type filename: str
        """
        routes.project_file.upload_project_file(token=self.token, project_id=project_id, file=file,
                                                filename=filename, base_url=self.base_url,
                                                timeout=self.file_upload_timeout)

    def upload_dfolder(self, project_id: str, folder_path: str, file_basename: str = None) -> None:
        """
        Uploads the .tdf and .tdfbin files from a bruker .d folder.
        :param project_id: The ID of the project.
        :type project_id: str
        :param folder_path: The path to the folder containing the .tdf and .tdfbin files.
        :type folder_path: str
        :param file_basename: The basename of the files to upload.
        :type file_basename: str
        """
        if file_basename is None:
            file_basename = os.path.basename(folder_path)

        files = os.listdir(folder_path)

        # check if .tdf and or .tdfbin files are present
        contains_tdf = any(file.endswith('.tdf') for file in files)
        contains_tdfbin = any(file.endswith('.tdfbin') for file in files)

        if not contains_tdf and not contains_tdfbin:
            raise ValueError(f"No .tdf or .tdfbin files found in {folder_path}")

        for file in files:
            if file.endswith('.tdf') or file.endswith('.tdf_bin'):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'rb') as f:
                    self.upload_project_file(project_id, f, file_basename + '.' + file)

    def upload_raw_file(self, project_id: str, file_path: str, file_basename: str = None) -> None:
        """
        Uploads a raw file to a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param file_path: The path to raw file to upload.
        :type file_path: str
        :param file_basename: The basename of the files to upload.
        :type file_basename: str
        """

        if file_basename is None:
            file_basename = os.path.basename(file_path)

        # check if file ends with .raw
        if not file_basename.endswith('.raw'):
            raise ValueError(f"File {file_basename} is not a .raw file.")

        with open(file_path, 'rb') as f:
            self.upload_project_file(project_id, f, file_basename)

    def submit_search(self, project_id: str, search_settings: Dict) -> None:
        """
        Submits a search request for a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param search_settings: The search settings configuration.
        :type search_settings: Dict
        :raises ValueError: If the database specified in the search settings is not found.
        """

        _ = models.SearchConfig.model_validate(search_settings)

        database_id = search_settings['database']['fasta']
        database = self.get_database(database_id)
        if database is None:
            raise ValueError(f"Database with id {database_id} not found.")

        routes.search_results.create_search(token=self.token, project_id=project_id, search_config=search_settings,
                                            base_url=self.base_url, timeout=self.timeout)

    def can_search(self, project_id: str) -> bool:
        """
        Checks if a project can be searched.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: True if the project can be searched, False otherwise.
        :rtype: bool
        """
        project_files = self.get_project_files(project_id)
        statuses = {file.job_status for file in project_files}
        self.logger.debug(f'Statuses: {statuses}')
        if 'SUCCEEDED' in statuses:
            return True
        return False

    def is_processing_files(self, project_id: str) -> bool:
        """
        Checks if a project is currently processing files.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: True if the project is processing files, False otherwise.
        :rtype: bool
        """
        project_files = self.get_project_files(project_id)
        statuses = {file.job_status for file in project_files}

        if 'FAILED' in statuses or 'SUCCEEDED' in statuses:
            return False

        return True

    def get_resource_usage(self) -> models.OrganizationUsage:
        """
        Retrieves the resource usage of the organization.

        :return: The OrganizationUsage model.
        :rtype: models.OrganizationUsage
        """
        usage_data = routes.organization_usage.get_organization_usage(token=self.token, base_url=self.base_url,
                                                                      timeout=self.timeout)
        return models.OrganizationUsage.model_validate(usage_data)

    def get_user_profile(self) -> models.Profile:
        """
        Retrieves the user's profile information.

        :return: The Profile model.
        :rtype: models.Profile
        """
        profile_data = routes.profile.get_profile(token=self.token, base_url=self.base_url, timeout=self.timeout)
        return models.Profile.model_validate(profile_data)

    def update_user_profile(self, first_name: str, last_name: str) -> None:
        """
        Updates the user's profile information.

        :param first_name: The user's first name.
        :type first_name: str
        :param last_name: The user's last name.
        :type last_name: str
        """
        data = {'first_name': first_name, 'last_name': last_name}
        routes.profile.update_profile(token=self.token, data=data, base_url=self.base_url, timeout=self.timeout)

    def get_spectra(self, search_result_id: str, filename: str, scannr: str) -> List[models.ScanData]:
        """
        Retrieves the spectra for a specific search result and scan number.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param filename: The filename of the spectra.
        :type filename: str
        :param scannr: The scan number.
        :type scannr: str
        :return: A list of spectra.
        :rtype: List[Dict[str, Any]]
        """
        data = routes.search_results.get_spectra(token=self.token, search_result_id=search_result_id, filename=filename,
                                                 scannr=scannr, base_url=self.base_url, timeout=self.timeout)
        return [models.ScanData.model_validate(scan) for scan in data]

    def get_psm_annotations(self, search_result_id: str, psm_id: int) -> List[models.FragmentData]:
        """
        Retrieves the PSM annotations for a specific search result and PSM ID.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param psm_id: The PSM ID.
        :type psm_id: int
        :return: A list of PSM annotations.
        :rtype: List[Dict[str, Any]]
        """
        data = routes.search_results.get_psm_annotations(token=self.token, search_result_id=search_result_id,
                                                         psm_id=psm_id, base_url=self.base_url, timeout=self.timeout)
        return [models.FragmentData.model_validate(fragment) for fragment in data]

    def get_peptide_results(self, search_result_id: str, query_id: str,
                            query_type: Literal['peptide', 'protein'] = 'protein') -> List[models.PeptideResult]:
        """
        Retrieves the peptides for a specific search result and protein ID.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param query_id: The protein ID, or peptide ID.
        :type query_id: str
        :param query_type: The type of query, either 'peptide' or 'protein'. Defaults to 'protein'.
        :type query_type: Literal['peptide', 'protein']
        :return: A list of peptides.
        :rtype: List[Dict[str, Any]]
        """

        if query_type == 'protein':
            data = routes.get_peptides_from_protein_id(token=self.token, search_result_id=search_result_id,
                                                       protein_id=query_id, base_url=self.base_url,
                                                       timeout=self.timeout)
        elif query_type == 'peptide':
            data = routes.get_peptides_from_peptide_id(token=self.token, search_result_id=search_result_id,
                                                       peptide_id=query_id, base_url=self.base_url,
                                                       timeout=self.timeout)
        else:
            raise ValueError(f'Invalid query type: {query_type}')

        return [models.PeptideResult.model_validate(peptide) for peptide in data]
