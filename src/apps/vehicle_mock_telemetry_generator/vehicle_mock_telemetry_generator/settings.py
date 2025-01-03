import logging.config
from pathlib import Path
from typing import Dict, List, Type

import yaml

from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName

from vehicle_geometry_intersection_ms_events.events import (
    VehicleArrivedToLoadingArea,
    VehicleDeparturedFromLoadingArea,
    VehicleDidMovementEvent,
)

BASE_DIR = Path(__file__).resolve().parent


def init_logging(logging_config_yaml_filepath: Path) -> None:
    with open(logging_config_yaml_filepath, 'r') as file:
        config = yaml.safe_load(file.read())

    logging.config.dictConfig(config)


init_logging(logging_config_yaml_filepath=BASE_DIR / 'logging_config.yaml')

KAFKA_BOOTSTRAP_SERVERS: List[str] = ['localhost:9092']

# TODO: переделать на автогенерацию
EVENTS_DISTRIBUTION_SCHEME_BY_TOPICS: Dict[Type[IntegrationEvent], List[TopicName]] = {
    VehicleArrivedToLoadingArea: ['vehicle_geometry_intersection_ms'],
    VehicleDeparturedFromLoadingArea: ['vehicle_geometry_intersection_ms'],
    VehicleDidMovementEvent: ['vehicle_geometry_intersection_ms'],
}
