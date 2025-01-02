from pathlib import Path
from typing import List, Type

from framework.iapp import IApp
from framework.integrations_events.schema import EventsSchema

BASE_DIR = Path(__file__).resolve().parent.parent

KAFKA_BOOTSTRAP_SERVERS: List[str] = ['localhost:9092']


def init_logging() -> None:
    import yaml
    import logging
    from logging import config as logging_config

    LOGGING_CONFIG_YAML_FILENAME = 'logging_config.yaml'
    LOGGIN_CONFIG_YAML_FILE_PATH = BASE_DIR / 'settings' / LOGGING_CONFIG_YAML_FILENAME

    with open(LOGGIN_CONFIG_YAML_FILE_PATH, 'r') as file:
        config = yaml.safe_load(file.read())

    logging_config.dictConfig(config)

    logger = logging.getLogger('settings')
    logger.debug('%s was used to configure logging', LOGGING_CONFIG_YAML_FILENAME)


def collect_apps() -> List[Type[IApp]]:
    from vehicle_geometry_intersection_ms.app import VehicleGeometryIntersectionMSApp

    return [VehicleGeometryIntersectionMSApp]


def generate_events_schema(apps: List[IApp]) -> EventsSchema:
    events_schema = EventsSchema()

    for app in apps:
        for event_cls in app.processed_events():
            events_schema.register(event_cls=event_cls, topics=[app.topic()])

    return events_schema


INSTALLED_APPS = collect_apps()

EVENT_SCHEMA = generate_events_schema(apps=INSTALLED_APPS)
