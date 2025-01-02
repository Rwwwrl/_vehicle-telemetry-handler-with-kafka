from collections import defaultdict
from typing import Dict, List, Type

from framework.kafka.hints import TopicName

from .integration_event import IntegrationEvent


# TODO: переименовать
class EventsSchema:
    def __init__(self):
        self._data: Dict[Type[IntegrationEvent], List[TopicName]] = defaultdict(list)

    def register(self, event_cls: Type[IntegrationEvent], topics: List[TopicName]) -> None:
        self._data[event_cls].extend(topics)

    def __getitem__(self, item: Type[IntegrationEvent]) -> List[TopicName]:
        return self._data[item]
