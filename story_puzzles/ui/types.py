from dataclasses import dataclass
from typing import Dict, Set, Optional, Tuple
from ..entity.template import BaseEntityTemplate
from ..scene.template import SceneTemplateTag
from ..scene import Scene

@dataclass
class SelectionState:
    """Represents the current state of entity selections"""
    selections: Dict[str, Tuple[SceneTemplateTag, BaseEntityTemplate]]  # tag_name -> (tag, entity)
    used_entities: Dict[str, Set[str]]  # entity_type -> set of entity names
    scene: Optional[Scene] = None

    def clear(self):
        """Clear all selections"""
        self.selections = {}
        self.used_entities = {}
        
    def remove_selection(self, tag_name: str):
        """Remove a specific selection and update used_entities"""
        if tag_name in self.selections:
            tag, entity = self.selections[tag_name]
            entity_type = entity.entity_type.value
            if entity_type in self.used_entities:
                self.used_entities[entity_type].remove(entity.name)
            del self.selections[tag_name]

    def add_selection(self, tag: SceneTemplateTag, entity: BaseEntityTemplate):
        """Add a new selection and update used_entities"""
        entity_type = entity.entity_type.value
        if entity_type not in self.used_entities:
            self.used_entities[entity_type] = set()
        self.used_entities[entity_type].add(entity.name)
        self.selections[tag.tag_name] = (tag, entity) 