from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, EnumField
from ..entity_template import *
from ..entity_template.types import EntityType

class BaseSceneEntity(Document):
    """ This is a scene instanced entity, it maps back to a BaseEntity"""
    meta = {'allow_inheritance': True}
    scene_tag = StringField(required=True)
    entity_type = EnumField(EntityType, required=True)
    

class SceneTemplateTag(Document):
    entity_type = EnumField(EntityType, required=True)
    tag = StringField(required=True)
    
    def matches_entity(self, entity: BaseSceneEntity) -> bool:
        if entity.entity_type != self.entity_type:
            return False
        return entity.scene_tag.endswith(f":{self.tag}}}")

    def get_formatted_tag(self) -> str:
        return f"{{{self.entity_type.value}:{self.tag}}}"

class Scene(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    template = StringField(required=True)
    entities = ListField(EmbeddedDocumentField(BaseSceneEntity))
    template_tags = ListField(EmbeddedDocumentField(SceneTemplateTag))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parse_template()

    def _parse_template(self) -> list[SceneTemplateTag]:
        """Parse the template string and saves a list of SceneTemplateTag objects."""
        template_tags = []
        current_pos = 0
        
        while True:
            # Find the next opening brace
            start = self.template.find('{', current_pos)
            if start == -1:
                break
            
            # Find the corresponding closing brace
            end = self.template.find('}', start)
            if end == -1:
                break
            
            # Extract the tag content
            tag_content = self.template[start + 1:end]
            
            # Split the content into type and identifier
            try:
                entity_type_str, identifier = tag_content.split(':', 1)
                entity_type_str = entity_type_str.lower()
                
                # Convert string to EntityType enum
                if entity_type_str == 'character':
                    entity_type = EntityType.CHARACTER
                elif entity_type_str == 'structure':
                    entity_type = EntityType.STRUCTURE
                elif entity_type_str == 'creature':
                    entity_type = EntityType.CREATURE
                elif entity_type_str == 'object':
                    entity_type = EntityType.OBJECT_PROP
                elif entity_type_str == 'landmark':
                    entity_type = EntityType.LANDMARK
                else:
                    # Skip verb tags or unknown types
                    current_pos = end + 1
                    continue
                
                template_tags.append(SceneTemplateTag(entity_type, identifier.strip()))
                
            except ValueError:
                # Skip malformed tags
                pass
            
            current_pos = end + 1
        
        self.template_tags = template_tags

    def add_entity_by_tag(self, entity: BaseEntity, template_tag: str):
        """
        Connects an entity to a template tag in the scene. Once this is conntected, the entity is
        no longer a BaseEntity, but a BaseSceneEntity. Only one entity can be connected to a template tag and 
        an entity can only be in any scene once.
        """
        if template_tag not in self.template:
            raise ValueError(f"Template tag {template_tag} not found in template {self.template}")
        
        # Parse template to get tag information
        template_tags = self._parse_template()
        matching_tag = None
        
        # Find the matching template tag
        for tag in template_tags:
            if tag.get_formatted_tag() == template_tag:
                matching_tag = tag
                break
        
        if not matching_tag:
            raise ValueError(f"Could not parse template tag {template_tag}")
        
        # Verify entity type matches the template tag type
        if not matching_tag.matches_entity(entity):
            raise TypeError(
                f"Entity type mismatch. Expected {matching_tag.entity_type.value}, "
                f"but got entity of type {type(entity).__name__}"
            )
        
        self.entities.append(entity)

    def get_entity_by_tag(self, template_tag: str) -> BaseSceneEntity:
        for entity in self.entities:
            if entity.scene_tag == template_tag:
                return entity
        raise ValueError(f"Template tag {template_tag} not found in scene {self.name}")
    
    def _is_entity_in_scene(self, entity: BaseSceneEntity) -> bool:
        for scene_entity in self.entities:
            if scene_entity.scene_tag == entity.scene_tag:
                return True
        return False
    
    def __str__(self):
        return f"Scene: {self.name}\nDescription: {self.description}\nTemplate: {self.template}\nEntities: {self.entities}"
