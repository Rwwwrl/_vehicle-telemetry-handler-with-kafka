import logging
from typing import Dict, List, NoReturn

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.structs import TopicPartition

from framework.common.secs_to_millisecs import secs_to_millisecs
from framework.integrations_events.integration_event_serde import IntegrationEventSerDe

from vehicle_geometry_intersection_ms import settings

logger = logging.getLogger(settings.MICROSERVICE_NAME)


def _run_kafka_consumer_polling() -> NoReturn:
    # TODO: заменить потом
    client_id = 'client_id'
    group_id = 'group_id'

    consumer = KafkaConsumer(
        settings.KAFKA_CONSUMER_POLLING_DETAILS.topic,
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
    _run_kafka_consumer_polling()


if __name__ == '__main__':
    main()
