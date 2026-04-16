import requests

from configuration.environment_configuration import self_hosted_registry_username, self_hosted_registry_password, \
    self_hosted_registry_url
from service.generic_service import GenericService


class SelfHostedRegistryService(GenericService):
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (self_hosted_registry_username, self_hosted_registry_password)
        self.headers = {
            "Accept": (
                "application/vnd.docker.distribution.manifest.v2+json,"
                "application/vnd.docker.distribution.manifest.list.v2+json,"
                "application/vnd.oci.image.manifest.v1+json,"
                "application/vnd.oci.image.index.v1+json"
            )
        }

    def retrieve_repositories(self):
        http_response = self.session.get(f"{self_hosted_registry_url}/v2/_catalog", headers=self.headers)
        http_response.raise_for_status()

        return http_response.json().get("repositories", [])

    def retrieve_repository_tags(self, repository):
        http_response = self.session.get(f"{self_hosted_registry_url}/v2/{repository}/tags/list", headers=self.headers)
        http_response.raise_for_status()

        return http_response.json().get("tags", [])

    def retrieve_repository_tag_last_date_and_digest(self, repository, tag):
        http_response = self.session.get(f"{self_hosted_registry_url}/v2/{repository}/manifests/{tag}",
                                         headers=self.headers)
        http_response.raise_for_status()

        date = http_response.headers.get("Date")
        docker_content_digest = http_response.headers.get("Docker-Content-Digest")

        # Classic Docker Image
        image_digest = http_response.json().get("config", {}).get("digest")
        if image_digest:
            http_response = self.session.get(f"{self_hosted_registry_url}/v2/{repository}/blobs/{image_digest}",
                                             headers=self.headers)
            http_response.raise_for_status()

            return self._parse_date_to_utc(http_response.json().get("created")).timestamp(), docker_content_digest

        # OCI Docker Image
        image_digest = http_response.json().get("manifests", [])[0].get("digest")
        if image_digest:
            http_response = self.session.get(f"{self_hosted_registry_url}/v2/{repository}/manifests/{image_digest}",
                                             headers=self.headers)
            http_response.raise_for_status()
            image_digest = http_response.json().get("config", {}).get("digest")
            http_response = self.session.get(f"{self_hosted_registry_url}/v2/{repository}/blobs/{image_digest}",
                                             headers=self.headers)
            http_response.raise_for_status()

            return self._parse_date_to_utc(http_response.json().get("created")).timestamp(), docker_content_digest
        return self._parse_date_to_utc(date).timestamp(), docker_content_digest

    def delete_repository_tag_by_digest(self, repository, digest):
        http_response = self.session.delete(f"{self_hosted_registry_url}/v2/{repository}/manifests/{digest}",
                                            headers=self.headers)
        http_response.raise_for_status()
        return http_response.status_code == 202

    def delete_repository_tag(self, repository, tag):
        pass

    def get_deletion_strategy(self):
        return "digest"
