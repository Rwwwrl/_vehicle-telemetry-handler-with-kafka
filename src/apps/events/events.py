from pydantic.types import PositiveFloat, PositiveInt

from framework.common.dto import DTO
from framework.kafka.integration_event import IntegrationEvent

__all__ = (
    'VehicleDidMovementEvent',
    'VehicleArrivedToLoadingAreaEvent',
    'VehicleDeparturedFromLoadingAreaEvent',
    'VehicleStartedLoadingEvent',
    'VehicleFinishedLoadingEvent',
)


class VehiclePositionLatLon(DTO):
    lat: PositiveFloat
    lon: PositiveFloat


class VehicleDidMovementEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    new_position: VehiclePositionLatLon


class VehicleArrivedToLoadingAreaEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt


class VehicleDeparturedFromLoadingAreaEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt


class VehicleStartedLoadingEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt


class VehicleFinishedLoadingEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt
