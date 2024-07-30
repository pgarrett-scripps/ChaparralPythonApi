"""
The Client class is a wrapper around the Chaparral API.
"""
import os
from typing import List, Optional, Dict, IO, Literal
import logging

import requests
from requests import HTTPError
from requests.exceptions import Timeout

from .constants import DEFAULT_BASE_URL
from . import models
from . import routes
from .custom_types import STATUS_TYPES, LOGGING_LEVELS
from .utils import get_best_chaparral_server


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
    :param base_url: The Chaparral API base URL. Defaults to DEFAULT_BASE_URL. If None, the best server is selected.
    :type base_url: str | None
    :param timeout: The request timeout in seconds. Defaults to 10 seconds.
    :type timeout: float | None
    :param file_upload_timeout: The timeout duration for file uploads in seconds. Defaults to 60 seconds.
    :type file_upload_timeout: float | None
    """

    def __init__(self, token: str, base_url: Optional[str] = DEFAULT_BASE_URL, timeout: Optional[float] = 10,
                 file_upload_timeout: Optional[float] = 120, log_level: LOGGING_LEVELS = 'INFO'):
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
        self.logger.info("Testing connection to the Chaparral API")
        try:
            self.get_user_profile()
            self.logger.info("Connection to the Chaparral API is successful")
            return True
        except HTTPError as e:
            self.logger.error(f"Connection to the Chaparral was unsuccessful: {e}")
            return False
        except Timeout as e:
            self.logger.error(f"Connection to the Chaparral timed out: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Connection to the Chaparral API failed: {e}")
            raise

    def get_projects(self) -> List[models.Project]:
        """
        Retrieves a list of projects.

        :return: A list of Project models.
        :rtype: List[models.Project]
        """
        self.logger.info("Retrieving list of projects")
        try:
            projects_data = routes.project.get_projects(token=self.token, base_url=self.base_url, timeout=self.timeout)
            self.logger.info("Projects retrieved successfully")
            self.logger.debug(f"Projects data: {projects_data}")
            return [models.Project.model_validate(project) for project in projects_data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve projects: {e}")
            raise

    def get_project(self, project_id: str) -> models.Project:
        """
        Retrieves a specific project by its ID.

        :param project_id: The ID of the project to retrieve.
        :type project_id: str
        :return: The Project model.
        :rtype: models.Project
        """
        self.logger.info(f"Retrieving project with ID: {project_id}")
        try:
            project_data = routes.project.get_project(token=self.token, project_id=project_id, base_url=self.base_url,
                                                      timeout=self.timeout)
            self.logger.info(f"Project {project_id} retrieved successfully")
            self.logger.debug(f"Project data: {project_data}")
            return models.Project.model_validate(project_data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve project {project_id}: {e}")
            raise

    def get_projects_by_tag(self, tag: str) -> List[models.Project]:
        """
        Retrieves projects that have a specific tag.

        :param tag: The tag to filter projects by.
        :type tag: str
        :return: A list of Project models that have the specified tag.
        :rtype: List[models.Project]
        """
        self.logger.info(f"Retrieving projects with tag: {tag}")
        try:
            projects = self.get_projects()
            tagged_projects = [project for project in projects if project.tags and tag in project.tags]
            self.logger.info(f"Projects with tag {tag} retrieved successfully")
            self.logger.debug(f"Tagged projects: {tagged_projects}")
            return tagged_projects
        except Exception as e:
            self.logger.error(f"Failed to retrieve projects with tag {tag}: {e}")
            raise

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
        self.logger.info(f"Creating a new project with name: {name}, description: {description}")
        data = {'name': name, 'description': description}
        try:
            project_data = routes.project.create_project(token=self.token, data=data, base_url=self.base_url,
                                                         timeout=self.timeout)
            self.logger.info(f"Project created successfully: {project_data}")
            self.logger.debug(f"Project data: {project_data}")
            return models.Project.model_validate(project_data)
        except Exception as e:
            self.logger.error(f"Failed to create project: {e}")
            raise

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
        self.logger.info(f"Updating project {project_id} with name: {name}, description: {description}, tags: {tags}")
        data = {'name': name, 'description': description, 'tags': tags}
        try:
            updated_data = routes.project.update_project(token=self.token, project_id=project_id, data=data,
                                                         base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"Project updated successfully: {updated_data}")
            return models.Project.model_validate(updated_data)
        except Exception as e:
            self.logger.error(f"Failed to update project {project_id}: {e}")
            raise

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
        self.logger.info(f"Tagging projects {project_ids} with tags: {tags}")
        projects = []
        for project in [self.get_project(project_id) for project_id in project_ids]:
            project.tags = tags
            if project.tags is None:
                project.tags = []
            try:
                updated_project = self.update_project(project.id, project.name, project.description,
                                                      project.tags + tags)
                projects.append(updated_project)
                self.logger.info(f"Project {project.id} tagged successfully")
                self.logger.debug(f"Updated project data: {updated_project}")
            except Exception as e:
                self.logger.error(f"Failed to tag project {project.id}: {e}")
        return projects

    def delete_project(self, project_id: str) -> None:
        """
        Deletes a project.

        :param project_id: The ID of the project to delete.
        :type project_id: str
        """
        self.logger.info(f"Deleting project {project_id}")
        try:
            routes.project.delete_project(token=self.token, project_id=project_id, base_url=self.base_url,
                                          timeout=self.timeout)
            self.logger.info(f"Project {project_id} deleted successfully")
        except Exception as e:
            self.logger.error(f"Failed to delete project {project_id}: {e}")
            raise

    def get_organization(self) -> models.Organization:
        """
        Retrieves the organization information.

        :return: The Organization model.
        :rtype: models.Organization
        """
        self.logger.info("Retrieving organization information")
        try:
            organization_data = routes.organization.get_organization(token=self.token, base_url=self.base_url,
                                                                     timeout=self.timeout)
            self.logger.info("Organization information retrieved successfully")
            self.logger.debug(f"Organization data: {organization_data}")
            return models.Organization.model_validate(organization_data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve organization information: {e}")
            raise

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
        self.logger.info(f"Updating organization {organization_id} with name: {name}")
        data = {'name': name}
        try:
            updated_data = routes.organization.update_organization(token=self.token, organization_id=organization_id,
                                                                   data=data, base_url=self.base_url,
                                                                   timeout=self.timeout)
            self.logger.info(f"Organization {organization_id} updated successfully")
            self.logger.debug(f"Updated organization data: {updated_data}")
            return models.Organization.model_validate(updated_data)
        except Exception as e:
            self.logger.error(f"Failed to update organization {organization_id}: {e}")
            raise

    def invite_to_organization(self, email: str) -> None:
        """
        Sends an invitation to join the organization.

        :param email: The email address to send the invitation to.
        :type email: str
        """
        self.logger.info(f"Sending invitation to {email} to join the organization")
        try:
            routes.organization_invite.create_organization_invite(token=self.token, data={'email': email},
                                                                  base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"Invitation sent successfully to {email}")
        except Exception as e:
            self.logger.error(f"Failed to send invitation to {email}: {e}")
            raise

    def get_databases(self) -> List[models.Database]:
        """
        Retrieves a list of databases.

        :return: A list of Database models.
        :rtype: List[models.Database]
        """
        self.logger.info("Retrieving list of databases")
        try:
            datas = routes.databases.get_databases(token=self.token, base_url=self.base_url, timeout=self.timeout)
            self.logger.info("Databases retrieved successfully")
            self.logger.debug(f"Databases data: {datas}")
            return [models.Database.model_validate(data) for data in datas]
        except Exception as e:
            self.logger.error(f"Failed to retrieve databases: {e}")
            raise

    def get_database(self, database_id: str) -> models.Database:
        """
        Retrieves a specific database by its ID.

        :param database_id: The ID of the database to retrieve.
        :type database_id: str
        :return: The Database model.
        :rtype: models.Database
        """
        self.logger.info(f"Retrieving database with ID: {database_id}")
        try:
            data = routes.databases.get_database(token=self.token, database_id=database_id, base_url=self.base_url,
                                                 timeout=self.timeout)
            self.logger.info(f"Database {database_id} retrieved successfully")
            self.logger.debug(f"Database data: {data}")
            return models.Database.model_validate(data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve database {database_id}: {e}")
            raise

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
        self.logger.info(
            f"Updating database {database_id} with name: {name}, organism: {organism}, decoy_tag: {decoy_tag}")
        data = {'name': name, 'organism': organism, 'decoy_tag': decoy_tag}
        try:
            updated_data = routes.databases.update_database(token=self.token, database_id=database_id, data=data,
                                                            base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"Database {database_id} updated successfully")
            self.logger.debug(f"Updated database data: {updated_data}")
            return models.Database.model_validate(updated_data)
        except Exception as e:
            self.logger.error(f"Failed to update database {database_id}: {e}")
            raise

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
        self.logger.info(f"Creating a new database with filename: {filename}")
        try:
            created_data = routes.databases.create_database(token=self.token, database_bytes=database_bytes,
                                                            filename=filename, base_url=self.base_url,
                                                            timeout=self.timeout)
            self.logger.info("Database created successfully")
            self.logger.debug(f"Created database data: {created_data}")
            return models.Database.model_validate(created_data)
        except Exception as e:
            self.logger.error(f"Failed to create database: {e}")
            raise

    def delete_database(self, database_id: str) -> None:
        """
        Deletes a database.

        :param database_id: The ID of the database to delete.
        :type database_id: str
        """
        self.logger.info(f"Deleting database with ID: {database_id}")
        try:
            routes.databases.delete_database(token=self.token, database_id=database_id, base_url=self.base_url,
                                             timeout=self.timeout)
            self.logger.info(f"Database {database_id} deleted successfully")
        except Exception as e:
            self.logger.error(f"Failed to delete database {database_id}: {e}")
            raise

    def get_search_results(self, status: Optional[STATUS_TYPES] = None) -> List[models.SearchResult]:
        """
        Retrieves a list of search results.

        :return: A list of SearchResult models.
        :rtype: List[models.SearchResult]
        """
        self.logger.info("Retrieving list of search results")
        try:
            results_data = routes.search_results.get_search_results(token=self.token, base_url=self.base_url,
                                                                    timeout=self.timeout)
            search_results = [models.SearchResult.model_validate(result) for result in results_data]
            self.logger.info("Search results retrieved successfully")
            self.logger.debug(f"Search results data: {search_results}")

            if status:
                filtered_results = [result for result in search_results if result.status == status]
                self.logger.info(f"Filtered search results by status: {status}")
                self.logger.debug(f"Filtered search results: {filtered_results}")
                return filtered_results

            return search_results
        except Exception as e:
            self.logger.error(f"Failed to retrieve search results: {e}")
            raise

    def get_search_result(self, search_result_id: str) -> Optional[models.SearchResult]:
        """
        Retrieves a specific search result by its ID.

        :param search_result_id: The ID of the search result to retrieve.
        :type search_result_id: str
        :return: The SearchResult model or None if not found.
        :rtype: Optional[models.SearchResult]
        """
        self.logger.info(f"Retrieving search result with ID: {search_result_id}")
        try:
            search_results = self.get_search_results()
            result = next((result for result in search_results if result.id == search_result_id), None)
            if result:
                self.logger.info(f"Search result {search_result_id} retrieved successfully")
                self.logger.debug(f"Search result data: {result}")
            else:
                self.logger.warning(f"Search result {search_result_id} not found")
            return result
        except Exception as e:
            self.logger.error(f"Failed to retrieve search result {search_result_id}: {e}")
            raise

    def get_search_result_download(self, search_result_id: str) -> models.SearchResultDownload:
        """
        Retrieves the search result download information by its ID.

        :param search_result_id: The ID of the search result download to retrieve.
        :type search_result_id: str
        :return: The SearchResultDownload model.
        :rtype: models.SearchResultDownload
        """
        self.logger.info(f"Retrieving search result download information for ID: {search_result_id}")
        try:
            result_download_data = routes.search_results_download.read_search_result_download(token=self.token,
                                                                                              search_result_id=search_result_id,
                                                                                              base_url=self.base_url,
                                                                                              timeout=self.timeout)
            self.logger.info(f"Search result download information for {search_result_id} retrieved successfully")
            return models.SearchResultDownload.model_validate(result_download_data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve search result download information for {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Fetching configuration JSON for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            config_json = _fetch_file(search_result_download.config_json, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(config_json)
                self.logger.info(
                    f"Configuration JSON for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(f"Configuration JSON for search result ID: {search_result_id} fetched successfully")
                return config_json
        except Exception as e:
            self.logger.error(f"Failed to fetch configuration JSON for search result ID: {search_result_id}: {e}")
            raise

    def fetch_matched_fragments_parquet(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[
        bytes]:
        """
        Fetches the matched fragments Parquet file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the matched fragments Parquet file or None if download_path is provided.
        :rtype: bytes | None
        """
        self.logger.info(f"Fetching matched fragments Parquet file for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            matched_fragments_parquet = _fetch_file(search_result_download.matched_fragments_parquet, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(matched_fragments_parquet)
                self.logger.info(
                    f"Matched fragments Parquet file for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(
                    f"Matched fragments Parquet file for search result ID: {search_result_id} fetched successfully")
                return matched_fragments_parquet
        except Exception as e:
            self.logger.error(
                f"Failed to fetch matched fragments Parquet file for search result ID: {search_result_id}: {e}")
            raise

    def fetch_peptide_csv(self, search_result_id: str, download_path: Optional[str] = None) -> Optional[bytes]:
        """
        Fetches the peptide CSV file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :param download_path: The path to save the downloaded file. Optional.
        :type download_path: str | None
        :return: The content of the peptide CSV file or None if download_path is provided.
        :rtype: bytes | None
        """
        self.logger.info(f"Fetching peptide CSV for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            peptide_csv = _fetch_file(search_result_download.peptide_csv, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(peptide_csv)
                self.logger.info(f"Peptide CSV for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(f"Peptide CSV for search result ID: {search_result_id} fetched successfully")
                return peptide_csv
        except Exception as e:
            self.logger.error(f"Failed to fetch peptide CSV for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Fetching proteins CSV for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            proteins_csv = _fetch_file(search_result_download.proteins_csv, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(proteins_csv)
                self.logger.info(f"Proteins CSV for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(f"Proteins CSV for search result ID: {search_result_id} fetched successfully")
                return proteins_csv
        except Exception as e:
            self.logger.error(f"Failed to fetch proteins CSV for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Fetching results JSON for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            results_json = _fetch_file(search_result_download.results_json, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(results_json)
                self.logger.info(f"Results JSON for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(f"Results JSON for search result ID: {search_result_id} fetched successfully")
                return results_json
        except Exception as e:
            self.logger.error(f"Failed to fetch results JSON for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Fetching results Parquet file for search result ID: {search_result_id}")
        try:
            search_result_download = self.get_search_result_download(search_result_id)
            results_parquet = _fetch_file(search_result_download.results_parquet, self.timeout)

            if download_path:
                with open(download_path, 'wb') as f:
                    f.write(results_parquet)
                self.logger.info(
                    f"Results Parquet file for search result ID: {search_result_id} saved to {download_path}")
            else:
                self.logger.info(f"Results Parquet file for search result ID: {search_result_id} fetched successfully")
                return results_parquet
        except Exception as e:
            self.logger.error(f"Failed to fetch results Parquet file for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Downloading all files for search result ID: {search_result_id} to folder: {download_folder}")

        if folder_name is None:
            folder_name = search_result_id

        download_path = os.path.join(download_folder, folder_name)
        os.makedirs(download_path, exist_ok=True)
        self.logger.info(f"Created download path: {download_path}")

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
            try:
                fetch_method(search_result_id=search_result_id, download_path=os.path.join(download_path, filename))
                self.logger.info(f"Downloaded {filename} for search result ID: {search_result_id}")
            except Exception as e:
                self.logger.error(f"Failed to download {filename} for search result ID: {search_result_id}: {e}")

    def get_qc_scores(self, search_result_id: str) -> List[models.QcScore]:
        """
        Retrieves the QC scores for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcScore models.
        :rtype: List[models.QcScore]
        """
        self.logger.info(f"Retrieving QC scores for search result ID: {search_result_id}")
        try:
            qc_scores_data = routes.search_result_qc.get_qc_scores(token=self.token, search_result_id=search_result_id,
                                                                   base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"QC scores for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"QC scores data: {qc_scores_data}")
            return [models.QcScore.model_validate(score) for score in qc_scores_data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve QC scores for search result ID: {search_result_id}: {e}")
            raise

    def get_qc_ids(self, search_result_id: str) -> List[models.QcId]:
        """
        Retrieves the QC IDs for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcId models.
        :rtype: List[models.QcId]
        """
        self.logger.info(f"Retrieving QC IDs for search result ID: {search_result_id}")
        try:
            qc_ids_data = routes.search_result_qc.get_qc_ids(token=self.token, search_result_id=search_result_id,
                                                             base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"QC IDs for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"QC IDs data: {qc_ids_data}")
            return [models.QcId.model_validate(qc_id) for qc_id in qc_ids_data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve QC IDs for search result ID: {search_result_id}: {e}")
            raise

    def get_qc_precursors(self, search_result_id: str) -> List[models.QcPrecursor]:
        """
        Retrieves the QC precursors for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: A list of QcPrecursor models.
        :rtype: List[models.QcPrecursor]
        """
        self.logger.info(f"Retrieving QC precursors for search result ID: {search_result_id}")
        try:
            qc_precursors_data = routes.search_result_qc.get_qc_precursors(token=self.token,
                                                                           search_result_id=search_result_id,
                                                                           base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"QC precursors for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"QC precursors data: {qc_precursors_data}")
            return [models.QcPrecursor.model_validate(precursor) for precursor in qc_precursors_data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve QC precursors for search result ID: {search_result_id}: {e}")
            raise

    def get_project_files(self, project_id: str) -> List[models.ProjectFile]:
        """
        Retrieves the files for a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: A list of ProjectFile models.
        :rtype: List[models.ProjectFile]
        """
        self.logger.info(f"Retrieving files for project ID: {project_id}")
        try:
            project_files_data = routes.project_file.get_project_files(token=self.token, project_id=project_id,
                                                                       base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"Files for project ID: {project_id} retrieved successfully")
            self.logger.debug(f"Project files data: {project_files_data}")
            return [models.ProjectFile.model_validate(file) for file in project_files_data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve files for project ID: {project_id}: {e}")
            raise

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
        self.logger.info(f"Retrieving file ID: {file_id} for project ID: {project_id}")
        try:
            raw_files = self.get_project_files(project_id)
            project_file = next((raw_file for raw_file in raw_files if raw_file.id == file_id), None)
            if project_file:
                self.logger.info(f"File ID: {file_id} for project ID: {project_id} retrieved successfully")
                self.logger.debug(f"Project file data: {project_file}")
            else:
                self.logger.warning(f"File ID: {file_id} for project ID: {project_id} not found")
            return project_file
        except Exception as e:
            self.logger.error(f"Failed to retrieve file ID: {file_id} for project ID: {project_id}: {e}")
            raise

    def upload_project_file(self, project_id: str, file: IO, filename: str) -> None:
        """
        Uploads a file to a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param file: The file to upload.
        :type file: IO
        :param filename: The name of the file to upload.
        :type filename: str
        """
        self.logger.info(f"Uploading file: {filename} to project ID: {project_id}")
        try:
            routes.project_file.upload_project_file(token=self.token, project_id=project_id, file=file,
                                                    filename=filename, base_url=self.base_url,
                                                    timeout=self.file_upload_timeout)
            self.logger.info(f"File: {filename} uploaded successfully to project ID: {project_id}")
        except Exception as e:
            self.logger.error(f"Failed to upload file: {filename} to project ID: {project_id}: {e}")
            raise

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
        self.logger.info(f"Uploading .tdf and .tdfbin files from folder {folder_path} to project ID: {project_id}")
        if file_basename is None:
            file_basename = os.path.basename(folder_path)

        files = os.listdir(folder_path)

        # check if .tdf and/or .tdfbin files are present
        contains_tdf = any(file.endswith('.tdf') for file in files)
        contains_tdfbin = any(file.endswith('.tdfbin') for file in files)

        if not contains_tdf and not contains_tdfbin:
            self.logger.error(f"No .tdf or .tdfbin files found in {folder_path}")
            raise ValueError(f"No .tdf or .tdfbin files found in {folder_path}")

        for file in files:
            if file.endswith('.tdf') or file.endswith('.tdf_bin'):
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'rb') as f:
                    try:
                        self.upload_project_file(project_id, f, file_basename + '.' + file)
                        self.logger.info(f"Uploaded file {file} to project ID: {project_id}")
                    except Exception as e:
                        self.logger.error(f"Failed to upload file {file} to project ID: {project_id}: {e}")
                        raise

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
        self.logger.info(f"Uploading raw file {file_path} to project ID: {project_id}")
        if file_basename is None:
            file_basename = os.path.basename(file_path)

        # check if file ends with .raw
        if not file_basename.endswith('.raw'):
            self.logger.error(f"File {file_basename} is not a .raw file")
            raise ValueError(f"File {file_basename} is not a .raw file.")

        try:
            with open(file_path, 'rb') as f:
                self.upload_project_file(project_id, f, file_basename)
            self.logger.info(f"Uploaded raw file {file_basename} to project ID: {project_id}")
        except Exception as e:
            self.logger.error(f"Failed to upload raw file {file_basename} to project ID: {project_id}: {e}")
            raise

    def submit_search(self, project_id: str, search_settings: Dict) -> None:
        """
        Submits a search request for a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param search_settings: The search settings configuration.
        :type search_settings: Dict
        :raises ValueError: If the database specified in the search settings is not found.
        """
        self.logger.info(f"Submitting search request for project ID: {project_id} with settings: {search_settings}")
        try:
            _ = models.SearchConfig.model_validate(search_settings)
            database_id = search_settings['database']['fasta']
            database = self.get_database(database_id)
            if database is None:
                self.logger.error(f"Database with id {database_id} not found")
                raise ValueError(f"Database with id {database_id} not found.")

            routes.search_results.create_search(token=self.token, project_id=project_id, search_config=search_settings,
                                                base_url=self.base_url, timeout=self.timeout)
            self.logger.info(f"Search request for project ID: {project_id} submitted successfully")
        except Exception as e:
            self.logger.error(f"Failed to submit search request for project ID: {project_id}: {e}")
            raise

    def can_search(self, project_id: str) -> bool:
        """
        Checks if a project can be searched.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: True if the project can be searched, False otherwise.
        :rtype: bool
        """
        self.logger.info(f"Checking if project ID: {project_id} can be searched")
        try:
            project_files = self.get_project_files(project_id)
            statuses = {file.job_status for file in project_files}
            self.logger.debug(f'Statuses: {statuses}')
            if 'SUCCEEDED' in statuses:
                self.logger.info(f"Project ID: {project_id} can be searched")
                return True
            self.logger.info(f"Project ID: {project_id} cannot be searched")
            return False
        except Exception as e:
            self.logger.error(f"Failed to check if project ID: {project_id} can be searched: {e}")
            raise

    def is_processing_files(self, project_id: str) -> bool:
        """
        Checks if a project is currently processing files.

        :param project_id: The ID of the project.
        :type project_id: str
        :return: True if the project is processing files, False otherwise.
        :rtype: bool
        """
        self.logger.info(f"Checking if project ID: {project_id} is processing files")
        try:
            project_files = self.get_project_files(project_id)
            statuses = {file.job_status for file in project_files}
            self.logger.debug(f"Statuses for project ID: {project_id}: {statuses}")
            if 'FAILED' in statuses or 'SUCCEEDED' in statuses:
                self.logger.info(f"Project ID: {project_id} is not processing files")
                return False
            self.logger.info(f"Project ID: {project_id} is processing files")
            return True
        except Exception as e:
            self.logger.error(f"Failed to check if project ID: {project_id} is processing files: {e}")
            raise

    def get_resource_usage(self) -> models.OrganizationUsage:
        """
        Retrieves the resource usage of the organization.

        :return: The OrganizationUsage model.
        :rtype: models.OrganizationUsage
        """
        self.logger.info("Retrieving resource usage of the organization")
        try:
            usage_data = routes.organization_usage.get_organization_usage(token=self.token, base_url=self.base_url,
                                                                          timeout=self.timeout)
            self.logger.info("Resource usage retrieved successfully")
            self.logger.debug(f"Resource usage data: {usage_data}")
            return models.OrganizationUsage.model_validate(usage_data)
        except Exception as e:
            self.logger.error("Failed to retrieve resource usage: {e}")
            raise

    def get_user_profile(self) -> models.Profile:
        """
        Retrieves the user's profile information.

        :return: The Profile model.
        :rtype: models.Profile
        """
        self.logger.info("Retrieving user profile information")
        try:
            profile_data = routes.profile.get_profile(token=self.token, base_url=self.base_url, timeout=self.timeout)
            self.logger.info("User profile information retrieved successfully")
            self.logger.debug(f"User profile data: {profile_data}")
            return models.Profile.model_validate(profile_data)
        except Exception as e:
            self.logger.error(f"Failed to retrieve user profile information: {e}")
            raise

    def update_user_profile(self, first_name: str, last_name: str) -> None:
        """
        Updates the user's profile information.

        :param first_name: The user's first name.
        :type first_name: str
        :param last_name: The user's last name.
        :type last_name: str
        """
        self.logger.info(f"Updating user profile information: {first_name} {last_name}")
        data = {'first_name': first_name, 'last_name': last_name}
        try:
            routes.profile.update_profile(token=self.token, data=data, base_url=self.base_url, timeout=self.timeout)
            self.logger.info("User profile updated successfully")
        except Exception as e:
            self.logger.error(f"Failed to update user profile: {e}")
            raise

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
        self.logger.info(
            f"Retrieving spectra for search result ID: {search_result_id}, filename: {filename}, scan number: {scannr}")
        try:
            data = routes.search_results.get_spectra(token=self.token, search_result_id=search_result_id,
                                                     filename=filename, scannr=scannr, base_url=self.base_url,
                                                     timeout=self.timeout)
            self.logger.info(f"Spectra for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"Spectra data: {data}")
            return [models.ScanData.model_validate(scan) for scan in data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve spectra for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(f"Retrieving PSM annotations for search result ID: {search_result_id}, PSM ID: {psm_id}")
        try:
            data = routes.search_results.get_psm_annotations(token=self.token, search_result_id=search_result_id,
                                                             psm_id=psm_id, base_url=self.base_url,
                                                             timeout=self.timeout)
            self.logger.info(f"PSM annotations for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"PSM annotations data: {data}")
            return [models.FragmentData.model_validate(fragment) for fragment in data]
        except Exception as e:
            self.logger.error(f"Failed to retrieve PSM annotations for search result ID: {search_result_id}: {e}")
            raise

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
        self.logger.info(
            f"Retrieving peptides for search result ID: {search_result_id}, query ID: {query_id}, query type: {query_type}")
        try:
            if query_type == 'protein':
                data = routes.get_peptides_from_protein_id(token=self.token, search_result_id=search_result_id,
                                                           protein_id=query_id, base_url=self.base_url,
                                                           timeout=self.timeout)
            elif query_type == 'peptide':
                data = routes.get_peptides_from_peptide_id(token=self.token, search_result_id=search_result_id,
                                                           peptide_id=query_id, base_url=self.base_url,
                                                           timeout=self.timeout)
            else:
                self.logger.error(f"Invalid query type: {query_type}")
                raise ValueError(f"Invalid query type: {query_type}")

            self.logger.info(f"Peptides for search result ID: {search_result_id} retrieved successfully")
            self.logger.debug(f"Peptides data: {data}")
            return [models.PeptideResult.model_validate(peptide) for peptide in data]
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve peptides for search result ID: {search_result_id}, query ID: {query_id}: {e}")
            raise
