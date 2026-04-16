import re

from configuration.environment_configuration import enabled_services
from service.dockerhub_personal_account_registry_service import DockerhubPersonalAccountRegistryService
from service.self_hosted_registry_service import SelfHostedRegistryService


def to_snake_case(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def snake_to_camel(string):
    return ''.join(word.capitalize() for word in string.split('_'))


def dynamic_create_service_instance(registry_service):
    module = __import__(f"service.{registry_service}_registry_service")
    service_class = getattr(module, snake_to_camel(registry_service) + "RegistryService")
    return service_class()


services = [dynamic_create_service_instance(enabled_service)
            for enabled_service in enabled_services]
