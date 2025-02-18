from mongoengine import Document, EmbeddedDocument, EnumField, StringField, ListField, EmbeddedDocumentField
from enum import Enum
# Enum for entity types
class EntityType(Enum):
    CHARACTER = "character"
    STRUCTURE = "structure"
    CREATURE = "creature"
    OBJECT_PROP = "object_prop"
    LANDMARK = "landmark"

class BaseSceneEntity(EmbeddedDocument):
    meta = {'allow_inheritance': True}
    scene_tag = StringField(required=True)
    entity_type = EnumField(EntityType, required=True)
    name = StringField(default="")
    description = StringField(default="")

class Character(BaseSceneEntity):
    entity_type = EnumField(EntityType, default=EntityType.CHARACTER)

class Structure(BaseSceneEntity):
    pass  # Inherits all fields from BaseSceneEntity

class Creature(BaseSceneEntity):
    pass

class ObjectProp(BaseSceneEntity):
    entity_type = EnumField(EntityType, default=EntityType.OBJECT_PROP)

class Landmark(BaseSceneEntity):
    entity_type = EnumField(EntityType, default=EntityType.LANDMARK)