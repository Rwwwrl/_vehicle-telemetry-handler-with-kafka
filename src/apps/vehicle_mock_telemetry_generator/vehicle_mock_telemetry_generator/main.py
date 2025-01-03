import logging
from typing import List

from framework.kafka import KafkaProducer
from framework.kafka.integration_event import IntegrationEvent

from vehicle_geometry_intersection_ms_events.events import (
    VehicleArrivedToLoadingArea,
    VehicleDeparturedFromLoadingArea,
    VehicleDidMovementEvent,
    VehiclePositionLatLon,
)

from vehicle_mock_telemetry_generator import settings

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


def _push_events_to_kafka(events: List[IntegrationEvent]) -> None:
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

    logger.debug(f'producer {producer} was initialized')

    for event in events:
        producer.send(event=event)

    producer.flush()
    producer.close()


def main() -> None:
    _push_events_to_kafka(events=_mock_events_v1())
    logger.debug('new events were pushed to Kafka')


if __name__ == '__main__':
    main()
