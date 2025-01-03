import logging.config
import operator
from pathlib import Path
from typing import List

import yaml

from event_distribution_scheme_by_topics.microservice_as_kafka_consumer_details import (
    EventProcessedByMicroservice,
    MicroserviceAsKafkaConsumerDetails,
    ProducingRequirements,
)

from events import (
    VehicleFinishedLoadingEvent,
    VehicleStartedLoadingEvent,
)

MICROSERVICE_NAME = 'vehicle_loading_unloading_ms'

BASE_DIR = Path(__file__).resolve().parent


def init_logging(logging_config_yaml_filepath: Path) -> None:
    with open(logging_config_yaml_filepath, 'r') as file:
        config = yaml.safe_load(file.read())

    logging.config.dictConfig(config)


init_logging(logging_config_yaml_filepath=BASE_DIR / 'logging_config.yaml')

MICROSERVICE_AS_KAFKA_CONSUMER_DETAILS = MicroserviceAsKafkaConsumerDetails(
    topicname=MICROSERVICE_NAME,
    events_processed_by_microservice=[
        EventProcessedByMicroservice(
            event_cls=VehicleStartedLoadingEvent,
            producing_requirements=ProducingRequirements(key=operator.attrgetter('vehicle_id')),
        ),
        EventProcessedByMicroservice(
            event_cls=VehicleFinishedLoadingEvent,
            producing_requirements=ProducingRequirements(key=operator.attrgetter('vehicle_id')),
        ),
    ],
)

KAFKA_BOOTSTRAP_SERVERS: List[str] = ['localhost:9092']
