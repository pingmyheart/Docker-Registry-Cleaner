# Docker-Registry-Cleaner
*Docker Registry Cleaner based on image tag and image age.*

![Last Commit](https://img.shields.io/github/last-commit/pingmyheart/Docker-Registry-Cleaner)
![Repo Size](https://img.shields.io/github/repo-size/pingmyheart/Docker-Registry-Cleaner)
![Issues](https://img.shields.io/github/issues/pingmyheart/Docker-Registry-Cleaner)
![Pull Requests](https://img.shields.io/github/issues-pr/pingmyheart/Docker-Registry-Cleaner)
![License](https://img.shields.io/github/license/pingmyheart/Docker-Registry-Cleaner)
![Top Language](https://img.shields.io/github/languages/top/pingmyheart/Docker-Registry-Cleaner)
![Language Count](https://img.shields.io/github/languages/count/pingmyheart/Docker-Registry-Cleaner)

## Features

- **Tag-Based Cleanup**: Remove images based on specific snapshot tags.
- **Age-Based Cleanup**: Automatically delete images that are older than a specified number of days
- **Self Hosted Registry Support**: Compatible with self-hosted Docker registries.
- **DockerHub Personal Account Support**: Can be used to clean up images in DockerHub personal accounts.

## Required Configuration

To use the cleaner, you need to set up a few required configurations:

1. **Days Cleanup Threshold**: Specify the number of days after which images should be considered for cleanup.
2. **Enabled Services**: Define which services (DockerHub, Self-Hosted Registry) should be cleaned up.
3. **DockerHub Personal Account Credentials**: If you want to clean up images in a DockerHub personal account, you need
   to provide your DockerHub username and a personal access token with the necessary permissions to manage your
   DockerHub repositories.
4. **Self-Hosted Registry Credentials**: If you want to clean up images in a self-hosted Docker registry, you need to
   provide the registry URL, along with a username and password that have the necessary permissions to manage the
   registry.

### Environment Variables Example

```bash
# Generic
DAYS_CLEANUP_INTERVAL=30
ENABLED_SERVICES=self_hosted,dockerhub_personal_account

# SelfHosted
SELF_HOSTED_REGISTRY_USERNAME=registry_username
SELF_HOSTED_REGISTRY_PASSWORD=strong_registry_password
SELF_HOSTED_REGISTRY_URL=https://my-personal-docker-registry.com


# DockerHub
DOCKERHUB_REGISTRY_USERNAME=dockerhub_username_not_email
DOCKERHUB_REGISTRY_PASSWORD=strong_dockerhub_password
DOCKERHUB_REGISTRY_URL=https://hub.docker.com
```

## Usage

Run the cleaner as a cron job or a scheduled task in your preferred environment. The cleaner will
automatically check for images that meet the specified cleanup criteria and remove them from the configured registries.
You can also run it manually whenever you want to perform a cleanup by executing the cleaner script with the appropriate
environment variables set.