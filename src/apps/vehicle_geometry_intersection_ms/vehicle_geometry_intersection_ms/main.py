import logging
from typing import Dict, List, NoReturn

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.structs import TopicPartition

from src import settings

from framework.common.secs_to_millisecs import secs_to_millisecs
from framework.integrations_events.integration_event_serde import IntegrationEventSerDe

from vehicle_geometry_intersection_ms.app import VehicleGeometryIntersectionMSApp

logger = logging.getLogger(VehicleGeometryIntersectionMSApp.app_name)


def _run_kafka_consumer_polling() -> NoReturn:
    client_id = f'kafka_consumer_{VehicleGeometryIntersectionMSApp.app_name}_1'
    group_id = VehicleGeometryIntersectionMSApp.app_name

    consumer = KafkaConsumer(
        VehicleGeometryIntersectionMSApp.topic(),
        client_id=client_id,
        group_id=group_id,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        enable_auto_commit=False,
    )

    logger.debug(f'consumer "{group_id}:{client_id}" has started')

    logger.debug('consumer is listening for new events...')

    while True:
        topic_partition_to_events: Dict[TopicPartition, List[ConsumerRecord]] = consumer.poll(
            max_records=10,
            timeout_ms=secs_to_millisecs(5),
        )
        if topic_partition_to_events:
            for topic_partition, events in topic_partition_to_events.items():
                logger.debug(f'there are {len(events)} new message in topic "{topic_partition.topic}"')

                for event in events:
                    event = IntegrationEventSerDe.deserialize(event_serialized_to_bytes=event.value)
                    logger.debug(f'new event: {repr(event)}')

            consumer.commit()
        else:
            logger.debug('there are no new events...')


def main() -> NoReturn:
    settings.init_logging()
    _run_kafka_consumer_polling()


if __name__ == '__main__':
    main()
