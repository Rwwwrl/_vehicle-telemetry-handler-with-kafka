import logging
from typing import List

from kafka import KafkaProducer

from event_distribution_scheme_by_topics_registry.events_distribution_scheme_by_topics import (
    EVENT_DISTRIBUTION_SCHEME_BY_TOPICS as _EVENT_DISTRIBUTION_SCHEME_BY_TOPICS,
)
from event_distribution_scheme_by_topics_registry.settings import EVENT_DISTRIBUTION_SCHEME_BY_TOPICS

from framework.integrations_events.integration_event import IntegrationEvent
from framework.integrations_events.integration_event_serde import IntegrationEventSerDe

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


def _push_events_to_kafka(
    events: List[IntegrationEvent],
    events_distribution_scheme_by_topics: _EVENT_DISTRIBUTION_SCHEME_BY_TOPICS,
) -> None:
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

    logger.debug(f'producer {producer} was initialized')

    for event in events:
        serialized_event = IntegrationEventSerDe.serialize(event=event)

        for topic in events_distribution_scheme_by_topics[type(event)]:
            producer.send(
                topic=topic,
                value=serialized_event,
            )

    producer.flush()
    producer.close()


def main() -> None:
    _push_events_to_kafka(
        events=_mock_events_v1(),
        events_distribution_scheme_by_topics=EVENT_DISTRIBUTION_SCHEME_BY_TOPICS,
    )
    logger.debug('new events were pushed to Kafka')


if __name__ == '__main__':
    main()
