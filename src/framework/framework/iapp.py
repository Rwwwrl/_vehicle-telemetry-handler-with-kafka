import abc
from typing import List, Type

from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName


class IApp(abc.ABC):
    @classmethod
    @property
    @abc.abstractmethod
    def app_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def processed_events(cls) -> List[Type[IntegrationEvent]]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def topic(cls) -> TopicName:
        raise NotImplementedError
