from typing import List, Type

from framework.common.dto import DTO
from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName


class KafkaConsumerPollingDetails(DTO):
    topic: TopicName
    """
    Топик, на который подписан микросервис
    """
    events_processed_by_microservice: List[Type[IntegrationEvent]]
    """
    Эвенты, которые обрабатывает микросервис
    """
