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
        
