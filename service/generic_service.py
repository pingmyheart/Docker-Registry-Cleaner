from abc import ABC, abstractmethod
from datetime import timezone

from dateutil import parser


class GenericService(ABC):
    """
    Implemented services, in order to be automatically picked by the automatic service selector,
    implemented class should be named as <SomethingLikeThatRegistryService> so the profile for the class
    will be something_like_that
    """

    @abstractmethod
    def retrieve_repositories(self):
        pass

    @abstractmethod
    def retrieve_repository_tags(self, repository):
        pass

    @abstractmethod
    def retrieve_repository_tag_last_date_and_digest(self, repository, tag):
        pass

    @abstractmethod
    def delete_repository_tag_by_digest(self, repository, digest):
        pass

    @abstractmethod
    def delete_repository_tag(self, repository, tag):
        pass

    @abstractmethod
    def get_deletion_strategy(self):
        pass

    def _parse_date_to_utc(self, date):
        dt = parser.parse(date)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc
