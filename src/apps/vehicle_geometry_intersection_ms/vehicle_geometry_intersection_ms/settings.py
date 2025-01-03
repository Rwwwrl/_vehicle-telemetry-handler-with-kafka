import logging.config
from pathlib import Path
from typing import List, Type

import yaml

from framework.common.dto import DTO
from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName

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


class KafkaConsumerPollingDetails(DTO):
    topic: TopicName
    """
    Топик, на который подписан микросервис
    """
    events_processed_by_microservice: List[Type[IntegrationEvent]]
    """
    Эвенты, которые обрабатывает микросервис
    """


KAFKA_CONSUMER_POLLING_DETAILS = KafkaConsumerPollingDetails(
    topic=MICROSERVICE_NAME,
    events_processed_by_microservice=[
        VehicleArrivedToLoadingArea,
        VehicleDeparturedFromLoadingArea,
        VehicleDidMovementEvent,
    ],
)

KAFKA_BOOTSTRAP_SERVERS: List[str] = ['localhost:9092']
