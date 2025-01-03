from typing import Dict, List, Type, Union

from framework.common.dto import DTO
from framework.kafka.hints import TopicName
from framework.kafka.integration_event import IntegrationEvent

from .microservice_as_kafka_consumer_details import ProducingRequirements


class TopicDTO(DTO):
    name: TopicName
    producing_requirements: Union[ProducingRequirements, None]


EventDistributionSchemeByTopics = Dict[Type[IntegrationEvent], List[TopicDTO]]
