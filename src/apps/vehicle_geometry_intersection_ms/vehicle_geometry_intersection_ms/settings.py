import logging.config
from pathlib import Path
from typing import List

import yaml

from event_distribution_scheme_by_topics_registry.kafka_consumer_polling_details import KafkaConsumerPollingDetails

from vehicle_geometry_intersection_ms_events.events import (
    VehicleArrivedToLoadingArea,
    VehicleDeparturedFromLoadingArea,
    VehicleDidMovementEvent,
)

MICROSERVICE_NAME = 'vehicle_geometry_intersection_ms'

BASE_DIR = Path(__file__).resolve().parent


def init_logging(logging_config_yaml_filepath: Path) -> None:
    with open(logging_config_yaml_filepath, 'r') as file:
        config = yaml.safe_load(file.read())

    logging.config.dictConfig(config)


init_logging(logging_config_yaml_filepath=BASE_DIR / 'logging_config.yaml')

KAFKA_CONSUMER_POLLING_DETAILS = KafkaConsumerPollingDetails(
    topic=MICROSERVICE_NAME,
    events_processed_by_microservice=[
        VehicleArrivedToLoadingArea,
        VehicleDeparturedFromLoadingArea,
        VehicleDidMovementEvent,
    ],
)

KAFKA_BOOTSTRAP_SERVERS: List[str] = ['localhost:9092']
