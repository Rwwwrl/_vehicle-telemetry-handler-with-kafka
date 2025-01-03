from collections import defaultdict
from typing import List

from event_distribution_scheme_by_topics_registry.kafka_consumer_polling_details import KafkaConsumerPollingDetails

from vehicle_geometry_intersection_ms.settings import (
    KAFKA_CONSUMER_POLLING_DETAILS as VehicleGeometryIntersectionMSKafkaConsumerPollingDetails,
)

from .events_distribution_scheme_by_topics import (
    EVENT_DISTRIBUTION_SCHEME_BY_TOPICS as _EVENT_DISTRIBUTION_SCHEME_BY_TOPICS,
)

# TODO: пока опустим момент как именно формируется этот список
MICROSERVICES_KAFKA_CONSUMER_POLLING_DETAILS: List[KafkaConsumerPollingDetails] = [
    VehicleGeometryIntersectionMSKafkaConsumerPollingDetails,
]


def _generate_event_distribution_scheme_by_topics() -> _EVENT_DISTRIBUTION_SCHEME_BY_TOPICS:
    result: _EVENT_DISTRIBUTION_SCHEME_BY_TOPICS = defaultdict(list)

    for kafka_consumer_polling_detail in MICROSERVICES_KAFKA_CONSUMER_POLLING_DETAILS:
        for event in kafka_consumer_polling_detail.events_processed_by_microservice:
            result[event].append(kafka_consumer_polling_detail.topic)

    return result


EVENT_DISTRIBUTION_SCHEME_BY_TOPICS = _generate_event_distribution_scheme_by_topics()
