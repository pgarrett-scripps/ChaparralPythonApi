"""
The Client class is a wrapper around the Chaparral API.
"""
from typing import List, Optional, Dict

import requests
from requests.exceptions import Timeout

from .constants import DEFAULT_BASE_URL
from . import models
from . import routes
from .utils import get_best_chaparral_server


def _fetch_file(url: str, timeout: Optional[int]) -> str:
    """
    Fetches the content of a file from a given URL.

    :param url: The URL of the file to fetch.
    :type url: str
    :param timeout: The timeout duration for the request in seconds.
    :type timeout: Optional[int]
    :return: The content of the file.
    :rtype: str
    :raises Timeout: If the request times out.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
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
                 file_upload_timeout: Optional[float] = 60):
        self.token = token

        if base_url is None:
            base_url = get_best_chaparral_server()

        self.base_url = base_url
        self.timeout = timeout
        self.file_upload_timeout = file_upload_timeout

    def get_projects(self) -> List[models.Project]:
        """
        Retrieves a list of projects.

        :return: A list of Project models.
        :rtype: List[models.Project]
        """
        projects_data = routes.project.get_projects(token=self.token, base_url=self.base_url, timeout=self.timeout)
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
        return [project for project in projects if tag in project.tags]

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
        result_data = routes.search_results.get_search_result(token=self.token, search_result_id=search_result_id,
                                                              base_url=self.base_url, timeout=self.timeout)
        return models.SearchResult.model_validate(result_data)

    def get_search_result_download(self, search_result_id: str) -> models.SearchResultDownload:
        """
        Retrieves the search result download information by its ID.

        :param search_result_id: The ID of the search result download to retrieve.
        :type search_result_id: str
        :return: The SearchResultDownload model.
        :rtype: models.SearchResultDownload
        """
        result_download_data = routes.search_results_download.read_search_result_download(token=self.token,
                                                                                          search_result_id=search_result_id,
                                                                                          base_url=self.base_url,
                                                                                          timeout=self.timeout)
        return models.SearchResultDownload.model_validate(result_download_data)

    def fetch_config_json(self, search_result_id: str) -> str:
        """
        Fetches the configuration JSON file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the configuration JSON file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        config_json = _fetch_file(search_result_download.config_json, self.timeout)
        return config_json

    def fetch_matched_fragments_parquet(self, search_result_id: str) -> str:
        """
        Fetches the matched fragments Parquet file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the matched fragments Parquet file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        matched_fragments_parquet = _fetch_file(search_result_download.matched_fragments_parquet, self.timeout)
        return matched_fragments_parquet

    def fetch_peptide_csv(self, search_result_id: str) -> str:
        """
        Fetches the peptide CSV file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the peptide CSV file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        peptide_csv = _fetch_file(search_result_download.peptide_csv, self.timeout)
        return peptide_csv

    def fetch_proteins_csv(self, search_result_id: str) -> str:
        """
        Fetches the proteins CSV file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the proteins CSV file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        proteins_csv = _fetch_file(search_result_download.proteins_csv, self.timeout)
        return proteins_csv

    def fetch_results_json(self, search_result_id: str) -> str:
        """
        Fetches the results JSON file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the results JSON file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        results_json = _fetch_file(search_result_download.results_json, self.timeout)
        return results_json

    def fetch_results_parquet(self, search_result_id: str) -> str:
        """
        Fetches the results Parquet file for a specific search result.

        :param search_result_id: The ID of the search result.
        :type search_result_id: str
        :return: The content of the results Parquet file.
        :rtype: str
        """
        search_result_download = self.get_search_result_download(search_result_id)
        results_parquet = _fetch_file(search_result_download.results_parquet, self.timeout)
        return results_parquet

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

    def upload_project_file(self, project_id: str, file_bytes: bytes, filename: str):
        """
        Uploads a file to a specific project.

        :param project_id: The ID of the project.
        :type project_id: str
        :param file_bytes: The bytes of the file to upload.
        :type file_bytes: bytes
        :param filename: The name of the file to upload.
        :type filename: str
        """
        routes.project_file.upload_project_file(token=self.token, project_id=project_id, file_bytes=file_bytes,
                                                filename=filename, base_url=self.base_url,
                                                timeout=self.file_upload_timeout)

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

    def update_user_profile(self, first_name: str, last_name: str) -> models.Profile:
        """
        Updates the user's profile information.

        :param first_name: The user's first name.
        :type first_name: str
        :param last_name: The user's last name.
        :type last_name: str
        :return: The updated Profile model.
        :rtype: models.Profile
        """
        data = {'first_name': first_name, 'last_name': last_name}
        updated_data = routes.profile.update_profile(token=self.token, data=data, base_url=self.base_url,
                                                     timeout=self.timeout)
        return models.Profile.model_validate(updated_data)
