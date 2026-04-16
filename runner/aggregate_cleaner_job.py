import re
from datetime import datetime, timezone

from configuration.environment_configuration import days_cleanup_interval
from configuration.logging_configuration import logger as log
from service import services


def run():
    for service in services:
        repositories = service.retrieve_repositories()
        for repository in repositories:
            tags = service.retrieve_repository_tags(repository)
            if tags:
                for tag in tags:
                    log.info(f"Scanning Repository: `{repository}`, Tag: `{tag}`")
                    if re.match(r".*-SNAPSHOT$", tag) or re.match(r".*.dev\d$", tag):
                        last_date, digest = service.retrieve_repository_tag_last_date_and_digest(
                            repository, tag)
                        now_iso_format = datetime.now(timezone.utc).timestamp()
                        if (int(now_iso_format) - int(last_date)) > 60 * 60 * 24 * days_cleanup_interval:
                            log.info(
                                f"\tTag `{tag}` in repository `{repository}` is a snapshot and last updated on `{datetime.fromtimestamp(last_date)}`. Deleting tag...")
                            if service.get_deletion_strategy() == "digest":
                                service.delete_repository_tag_by_digest(repository, digest)
                            elif service.get_deletion_strategy() == "tag":
                                service.delete_repository_tag(repository, tag)
                            else:
                                log.info(
                                    f"\tDeletion strategy `{service.get_deletion_strategy()}` is not supported. Skipping deletion of tag `{tag}` in repository `{repository}`.")
