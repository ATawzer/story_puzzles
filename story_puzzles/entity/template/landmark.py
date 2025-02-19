from mongoengine import EnumField
from .base import BaseEntityTemplate
from .types import EntityType

class LandmarkTemplate(BaseEntityTemplate):
    entity_type = EnumField(EntityType, default=EntityType.LANDMARK)
