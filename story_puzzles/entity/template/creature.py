from mongoengine import EnumField
from .base import BaseEntityTemplate
from .types import EntityType

class CreatureTemplate(BaseEntityTemplate):
    entity_type = EnumField(EntityType, default=EntityType.CREATURE) 