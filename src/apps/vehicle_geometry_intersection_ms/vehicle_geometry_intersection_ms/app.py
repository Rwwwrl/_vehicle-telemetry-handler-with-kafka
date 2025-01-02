from typing import List, Type

from framework.iapp import IApp
from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName

from vehicle_geometry_intersection_ms_events.events import (
    VehicleArrivedToLoadingArea,
    VehicleDeparturedFromLoadingArea,
    VehicleDidMovementEvent,
)


class VehicleGeometryIntersectionMSApp(IApp):
    app_name = 'vehicle_geometry_intersection_ms'

    @classmethod
    def processed_events(cls) -> List[Type[IntegrationEvent]]:
        # TODO: эвенты нужно собирать автоматически
        return [
            VehicleDidMovementEvent,
            VehicleArrivedToLoadingArea,
            VehicleDeparturedFromLoadingArea,
        ]

    @classmethod
    def topic(cls) -> TopicName:
        return cls.app_name
