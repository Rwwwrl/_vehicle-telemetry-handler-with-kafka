from typing import Dict, Generator, List

from kafka import KafkaConsumer as LibKafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.structs import TopicPartition

from framework.common.secs_to_millisecs import secs_to_millisecs
from framework.integrations_events.integration_event import IntegrationEvent
from framework.integrations_events.integration_event_serde import IntegrationEventSerDe

from .hints import TopicName

__all__ = ('KafkaConsumer', )


class KafkaConsumer:
    def __init__(self, topic: TopicName, client_id: str, group_id: str, bootstrap_servers: List[str]):
        self._lib_kafka_consumer = LibKafkaConsumer(
            topic,
            client_id=client_id,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            enable_auto_commit=False,
        )

    def poll(self, max_records: int, timeout_secs: float) -> Generator[List[IntegrationEvent], None, None]:
        while True:
            topic_partition_to_events: Dict[TopicPartition, List[ConsumerRecord]] = self._lib_kafka_consumer.poll(
                max_records=max_records,
                timeout_ms=secs_to_millisecs(timeout_secs),
            )
            if topic_partition_to_events:
                for events in topic_partition_to_events.values():
                    yield [IntegrationEventSerDe.deserialize(event.value) for event in events]

                self._lib_kafka_consumer.commit()
