from dataclasses import dataclass
from enum import Enum
# Enum for entity types
class EntityType(Enum):
    CHARACTER = "character"
    STRUCTURE = "structure"
    CREATURE = "creature"
    OBJECT_PROP = "object_prop"
    LANDMARK = "landmark"

@dataclass
class BaseSceneEntity:
    scene_tag: str  # required parameter first
    entity_type: EntityType
    name: str = ""  # optional parameter with default after
    description: str = ""

@dataclass
class Character(BaseSceneEntity):
    entity_type: EntityType = EntityType.CHARACTER

@dataclass
class Structure(BaseSceneEntity):
    name: str
    description: str = ""

@dataclass
class Creature(BaseSceneEntity):
    name: str
    description: str = ""

@dataclass
class ObjectProp(BaseSceneEntity):
    name: str
    description: str = ""

@dataclass
class Landmark(BaseSceneEntity):
    name: str
    description: str = ""