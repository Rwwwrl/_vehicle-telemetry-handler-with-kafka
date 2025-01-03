from typing import List

from kafka import KafkaProducer as LibKafkaProducer

from event_distribution_scheme_by_topics_registry.settings import EVENT_DISTRIBUTION_SCHEME_BY_TOPICS

from framework.integrations_events.integration_event import IntegrationEvent
from framework.integrations_events.integration_event_serde import IntegrationEventSerDe

__all__ = ('KafkaProducer', )


class KafkaProducer:
    def __init__(self, bootstrap_servers: List[str]):
        self._lib_kafka_producer = LibKafkaProducer(bootstrap_servers=bootstrap_servers)
        self._events_distrubution_scheme_by_topics = EVENT_DISTRIBUTION_SCHEME_BY_TOPICS

    def send(self, event: IntegrationEvent) -> None:
        serialized_to_bytes_event = IntegrationEventSerDe.serialize(event=event)
        for topic in self._events_distrubution_scheme_by_topics[type(event)]:
            self._lib_kafka_producer.send(
                topic=topic,
                value=serialized_to_bytes_event,
            )

    def flush(self) -> None:
        self._lib_kafka_producer.flush()

    def close(self) -> None:
        self._lib_kafka_producer.close()
