from .template import SceneTemplate, SceneTemplateTag
from ..entity.template import BaseEntityTemplate

class BaseSceneEntity:
    """ This is a scene instanced entity, it maps a template tag in a scene template
    to a BaseEntity that is filling it.
    """
    
    def __init__(self, entity: BaseEntityTemplate, template_tag: SceneTemplateTag):
        self.entity = entity
        self.template_tag = template_tag
    
class Scene:
    """
    An instance of a scene. The player will be able to see this scene and fill
    in the template tags with entities.
    """

    def __init__(self, scene_template: SceneTemplate):
        self.scene_template = scene_template
        self.entities = []

    def create_entity_by_tag(self, tag: SceneTemplateTag, entity: BaseEntityTemplate):
        """Add an entity to the scene by its tag."""
        if tag.is_valid_option(entity) and not self.is_entity_in_scene(entity):
            self.entities.append(BaseSceneEntity(entity, tag))
        
    def is_entity_in_scene(self, entity: 'BaseEntityTemplate') -> bool:
        """Check if an entity is already in the scene."""
        return any(scene_entity.entity.name == entity.name for scene_entity in self.entities)

    def get_tags_by_sentence(self) -> dict[int, list[SceneTemplateTag]]:
        """Group template tags by sentence number, pass through to scene template."""
        return self.scene_template.get_tags_by_sentence()

    def get_filled_description(self) -> str:
        """Generate the scene description with all tags replaced with entity names."""
        description = self.scene_template.template_description
        
        # Sort entities by tag position to replace from end to start
        # (to avoid messing up string positions)
        sorted_entities = sorted(
            self.entities, 
            key=lambda e: description.find(f"{{{e.template_tag.entity_type.value}:{e.template_tag.tag_name}}}")
        )
        
        # Replace each tag with its entity name
        for scene_entity in reversed(sorted_entities):
            tag_str = f"{{{scene_entity.template_tag.entity_type.value}:{scene_entity.template_tag.tag_name}}}"
            description = description.replace(tag_str, scene_entity.entity.name)
            
        return description

        
