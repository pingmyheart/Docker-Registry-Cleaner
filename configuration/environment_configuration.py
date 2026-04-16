import os

from dotenv import load_dotenv

load_dotenv()

# Generic config
days_cleanup_interval = int(os.getenv("DAYS_CLEANUP_INTERVAL", 30))
enabled_services = os.getenv("ENABLED_SERVICES").split(",")

# Self Hosted Docker Registry
self_hosted_registry_username = os.getenv("SELF_HOSTED_REGISTRY_USERNAME")
self_hosted_registry_password = os.getenv("SELF_HOSTED_REGISTRY_PASSWORD")
self_hosted_registry_url = os.getenv("SELF_HOSTED_REGISTRY_URL")

# DockerHub Registry
dockerhub_registry_username = os.getenv("DOCKERHUB_REGISTRY_USERNAME")
dockerhub_registry_password = os.getenv("DOCKERHUB_REGISTRY_PASSWORD")
dockerhub_registry_url = os.getenv("DOCKERHUB_REGISTRY_URL", "https://index.docker.io/v2/")
dockerhub_organization = os.getenv("DOCKERHUB_ORGANIZATION")  # Organization name if scan type is organization
