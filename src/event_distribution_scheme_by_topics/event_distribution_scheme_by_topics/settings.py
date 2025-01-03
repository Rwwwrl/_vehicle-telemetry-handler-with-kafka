from collections import defaultdict
from typing import List

import vehicle_geometry_intersection_ms.settings

from .events_distribution_scheme_by_topics import EventDistributionSchemeByTopics, TopicDTO
from .microservice_as_kafka_consumer_details import MicroserviceAsKafkaConsumerDetails

# TODO: пока опустим момент как именно формируется этот список
MICROSERVICES_AS_KAFKA_CONSUMERS_DETAILS: List[MicroserviceAsKafkaConsumerDetails] = [
    vehicle_geometry_intersection_ms.settings.MICROSERVICE_AS_KAFKA_CONSUMER_DETAILS,
]


def _generate_event_distribution_scheme_by_topics() -> EventDistributionSchemeByTopics:
    result: EventDistributionSchemeByTopics = defaultdict(list)

    for kafka_microservice_as_consumer_details in MICROSERVICES_AS_KAFKA_CONSUMERS_DETAILS:
        for event_processed_by_microservice in kafka_microservice_as_consumer_details.events_processed_by_microservice:
            result[event_processed_by_microservice.event_cls].append(
                TopicDTO(
                    name=kafka_microservice_as_consumer_details.topicname,
                    producing_requirements=event_processed_by_microservice.producing_requirements,
                ),
            )

    return result


EVENT_DISTRIBUTION_SCHEME_BY_TOPICS = _generate_event_distribution_scheme_by_topics()
