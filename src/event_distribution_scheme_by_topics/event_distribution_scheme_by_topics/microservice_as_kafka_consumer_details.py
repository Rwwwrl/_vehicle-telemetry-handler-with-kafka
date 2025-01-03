from typing import Callable, Hashable, List, Self, Type, Union

from pydantic import Field, model_validator

from framework.common.dto import DTO
from framework.kafka.hints import TopicName
from framework.kafka.integration_event import IntegrationEvent


def default_key(event: IntegrationEvent) -> Union[Hashable, None]:
    return None


def default_partition(event: IntegrationEvent) -> Union[int, None]:
    return None


class ProducingRequirements(DTO):

    key: Callable[[IntegrationEvent], Union[Hashable, None]] = Field(default=default_key)
    partition: Callable[[IntegrationEvent], Union[int, None]] = Field(default=default_partition)

    @model_validator(mode='after')
    def _validate_that_key_and_partition_are_not_specified_at_the_same_time(self) -> Self:
        if (self.key is not default_key) and (self.partition is not default_partition):
            raise ValueError('key and partition fields cannon be specified at the same time')

        return self


class EventProcessedByMicroservice(DTO):
    event_cls: Type[IntegrationEvent]
    producing_requirements: Union[ProducingRequirements, None]


class MicroserviceAsKafkaConsumerDetails(DTO):
    topicname: TopicName
    """
    Топик, на который подписан микросервис
    """
    events_processed_by_microservice: List[EventProcessedByMicroservice]
    """
    Эвенты, которые обрабатывает микросервис
    """
