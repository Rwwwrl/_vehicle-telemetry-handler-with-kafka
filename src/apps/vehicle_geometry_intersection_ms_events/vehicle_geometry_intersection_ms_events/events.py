from pydantic.types import PositiveFloat, PositiveInt

from framework.common.dto import DTO
from framework.kafka.integration_event import IntegrationEvent


class VehiclePositionLatLon(DTO):
    lat: PositiveFloat
    lon: PositiveFloat


class VehicleDidMovementEvent(IntegrationEvent):
    vehicle_id: PositiveInt
    new_position: VehiclePositionLatLon


class VehicleArrivedToLoadingArea(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt


class VehicleDeparturedFromLoadingArea(IntegrationEvent):
    vehicle_id: PositiveInt
    loading_area_id: PositiveInt
