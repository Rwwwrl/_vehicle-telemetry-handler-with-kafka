import json

from .integration_event import IntegrationEvent


class SerDe:
    @classmethod
    def serialize(cls, event: IntegrationEvent) -> bytes:
        as_dict = {
            'event_name': event.__class__.__name__,
            'data': event.model_dump(mode='python'),
        }
        return json.dumps(as_dict).encode()

    def deserialize(event_as_bytes: bytes) -> IntegrationEvent:
        # TODO: реализовать
        raise NotImplementedError
