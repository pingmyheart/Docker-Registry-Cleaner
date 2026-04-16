import requests

from configuration.environment_configuration import dockerhub_registry_url, dockerhub_registry_username, \
    dockerhub_registry_password
from service.generic_service import GenericService


class DockerhubPersonalAccountRegistryService(GenericService):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        http_response = self.session.post(f"{dockerhub_registry_url}/v2/users/login",
                                          data={"username": dockerhub_registry_username,
                                                "password": dockerhub_registry_password})
        http_response.raise_for_status()
        self.session.headers = {
            "Authorization": f"Bearer {http_response.json().get('token')}"
        }

    def retrieve_repositories(self):
        repos = []
        url = f"{dockerhub_registry_url}/v2/repositories/{dockerhub_registry_username}"
        while url:
            http_response = self.session.get(url)
            http_response.raise_for_status()

            data = http_response.json()
            repos.extend(data.get("results", []))

            url = data.get("next")

        return [repo.get("name") for repo in repos]

    def retrieve_repository_tags(self, repository):
        tags = []
        url = f"{dockerhub_registry_url}/v2/namespaces/{dockerhub_registry_username}/repositories/{repository}/tags"

        while url:
            http_response = self.session.get(url)
            http_response.raise_for_status()

            data = http_response.json()
            tags.extend(data.get("results", []))

            url = data.get("next")

        return [tag.get("name") for tag in tags]

    def retrieve_repository_tag_last_date_and_digest(self, repository, tag):
        http_response = self.session.get(
            f"{dockerhub_registry_url}/v2/namespaces/{dockerhub_registry_username}/repositories/{repository}/tags/{tag}")
        http_response.raise_for_status()

        data = http_response.json()
        return self._parse_date_to_utc(data.get("last_updated")).timestamp(), data.get("images", [])[0].get("digest")

    def delete_repository_tag_by_digest(self, repository, digest):
        # Unused since dockerhub delete by repo name and tag
        pass

    def delete_repository_tag(self, repository, tag):
        http_response = self.session.delete(
            f"{dockerhub_registry_url}/v2/repositories/{dockerhub_registry_username}/{repository}/tags/{tag}")
        http_response.raise_for_status()
        return http_response.status_code == 204

    def get_deletion_strategy(self):
        return "tag"
