import importlib
import json
from typing import NewType, Type

from .integration_event import IntegrationEvent

EventSerializedToBytes = NewType('EventSerializedToBytes', bytes)


def _get_absolute_path_for_event_cls(event_cls: Type[IntegrationEvent]) -> str:
    return f"{event_cls.__module__}.{event_cls.__qualname__}"


def _import_event_cls_by_absolute_path(absolute_path: str) -> Type[IntegrationEvent]:
    module_path, class_name = absolute_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class IntegrationEventSerDe:
    @classmethod
    def serialize(cls, event: IntegrationEvent) -> EventSerializedToBytes:
        as_dict = {
            '__event_cls_absolute_path': _get_absolute_path_for_event_cls(event_cls=type(event)),
            'data': event.model_dump(mode='python'),
        }
        return json.dumps(as_dict).encode()

    def deserialize(event_serialized_to_bytes: EventSerializedToBytes) -> IntegrationEvent:
        as_dict = json.loads(event_serialized_to_bytes)
        event_cls = _import_event_cls_by_absolute_path(absolute_path=as_dict['__event_cls_absolute_path'])
        return event_cls.model_validate(as_dict['data'])
