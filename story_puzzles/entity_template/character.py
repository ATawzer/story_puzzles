from mongoengine import EnumField
from .base import BaseEntityTemplate
from .types import EntityType

class CharacterTemplate(BaseEntityTemplate):
    entity_type = EnumField(EntityType, default=EntityType.CHARACTER)
