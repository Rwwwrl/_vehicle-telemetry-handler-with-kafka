import logging
from typing import NoReturn

from framework.kafka import KafkaConsumer

from vehicle_loading_unloading_ms import settings

logger = logging.getLogger(settings.MICROSERVICE_NAME)


def _run_kafka_consumer_polling() -> NoReturn:
    # TODO: заменить потом
    client_id = 'client_id'
    group_id = settings.MICROSERVICE_NAME

    consumer = KafkaConsumer(
        topic=settings.MICROSERVICE_AS_KAFKA_CONSUMER_DETAILS.topicname,
        client_id=client_id,
        group_id=group_id,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    )

    logger.debug(f'kafka consumer "{group_id}:{client_id}" has started')

    logger.debug('kafka consumer is listening for new events...')

    for batch_of_new_events in consumer.poll(max_records=10, timeout_secs=5):
        for event in batch_of_new_events:
            logger.debug(repr(event))


def main() -> NoReturn:
    _run_kafka_consumer_polling()


if __name__ == '__main__':
    main()
