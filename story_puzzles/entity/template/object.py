from mongoengine import EnumField
from .base import BaseEntityTemplate
from .types import EntityType

class ObjectPropTemplate(BaseEntityTemplate):
    entity_type = EnumField(EntityType, default=EntityType.OBJECT_PROP)
