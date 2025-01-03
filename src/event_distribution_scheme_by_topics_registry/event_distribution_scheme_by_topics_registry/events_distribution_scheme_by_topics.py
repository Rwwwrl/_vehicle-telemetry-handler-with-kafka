from typing import Dict, List, Type

from framework.integrations_events.integration_event import IntegrationEvent
from framework.kafka.hints import TopicName

EVENT_DISTRIBUTION_SCHEME_BY_TOPICS = Dict[Type[IntegrationEvent], List[TopicName]]
