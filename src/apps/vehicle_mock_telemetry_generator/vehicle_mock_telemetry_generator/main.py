import logging
from typing import List

from kafka import KafkaProducer

from src import settings

from framework.integrations_events.integration_event import IntegrationEvent
from framework.integrations_events.schema import EventsSchema
from framework.integrations_events.serde import SerDe

from vehicle_geometry_intersection_ms_events.events import (
    VehicleArrivedToLoadingArea,
    VehicleDeparturedFromLoadingArea,
    VehicleDidMovementEvent,
    VehiclePositionLatLon,
)

logger = logging.getLogger('vehicle_mock_telemetry_generator')


def _mock_events_v1() -> List[IntegrationEvent]:
    return [
        VehicleDidMovementEvent(
            vehicle_id=1,
            new_position=VehiclePositionLatLon(lat=10.0, lon=10.0),
        ),
        VehicleArrivedToLoadingArea(
            vehicle_id=1,
            loading_area_id=1,
        ),
        VehicleDeparturedFromLoadingArea(
            vehicle_id=1,
            loading_area_id=1,
        ),
        VehicleDidMovementEvent(
            vehicle_id=1,
            new_position=VehiclePositionLatLon(lat=20.0, lon=20.0),
        ),
    ]


def _push_events_to_kafka(events: List[IntegrationEvent], events_schema: EventsSchema) -> None:
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

    logger.debug(f'producer {producer} was initialized')

    for event in events:
        serialized_event = SerDe.serialize(event=event)

        for topic in events_schema[type(event)]:
            producer.send(
                topic=topic,
                value=serialized_event,
            )

    producer.flush()
    producer.close()


def main() -> None:
    settings.init_logging()
    _push_events_to_kafka(
        events=_mock_events_v1(),
        events_schema=settings.EVENT_SCHEMA,
    )
    logger.debug('new events were pushed to Kafka')


if __name__ == '__main__':
    main()
