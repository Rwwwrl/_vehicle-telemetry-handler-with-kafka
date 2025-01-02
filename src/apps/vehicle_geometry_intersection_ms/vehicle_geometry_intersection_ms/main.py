import json
import logging
from typing import Dict, List, NoReturn

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.structs import TopicPartition

from src import settings

from framework.common.dto import DTO
from framework.common.secs_to_millisecs import secs_to_millisecs

from vehicle_geometry_intersection_ms.app import VehicleGeometryIntersectionMSApp

logger = logging.getLogger(VehicleGeometryIntersectionMSApp.app_name)


class ReceivedMessageData(DTO):
    event_name: str
    data: dict


class ReceivedMessage(DTO):
    topic: str
    partition: int
    data: ReceivedMessageData


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
        topic_partition_to_messages: Dict[TopicPartition, List[ConsumerRecord]] = consumer.poll(
            max_records=10,
            timeout_ms=secs_to_millisecs(5),
        )
        if topic_partition_to_messages:
            for topic_partition, messages in topic_partition_to_messages.items():
                logger.debug(f'there are {len(messages)} new message in topic "{topic_partition.topic}"')

                for message in messages:
                    message_value: dict = json.loads(message.value)
                    received_message_data = ReceivedMessage(
                        data=ReceivedMessageData(
                            event_name=message_value['event_name'],
                            data=message_value['data'],
                        ),
                        partition=message.partition,
                        topic=message.topic,
                    )
                    logger.debug(f'received message: {repr(received_message_data)}')

            consumer.commit()
        else:
            logger.debug('there are no new messages...')


def main() -> NoReturn:
    settings.init_logging()
    _run_kafka_consumer_polling()


if __name__ == '__main__':
    main()
