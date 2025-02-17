from .entity import *

class SceneTemplateTag:
    def __init__(self, entity_type: EntityType, tag: str):
        self.entity_type = entity_type
        self.tag = tag

    def matches_entity(self, entity: BaseSceneEntity) -> bool:
        """Check if the given entity matches this template tag's type."""
        # Direct class checks
        if isinstance(entity, Character) and self.entity_type == EntityType.CHARACTER:
            return True
        if isinstance(entity, Structure) and self.entity_type == EntityType.STRUCTURE:
            return True
        if isinstance(entity, Creature) and self.entity_type == EntityType.CREATURE:
            return True

        # For other types, check the entity's scene_tag
        if isinstance(entity, BaseSceneEntity):
            try:
                entity_tag_parts = entity.scene_tag.strip("{}").split(":", 1)
                if len(entity_tag_parts) == 2:
                    type_str = entity_tag_parts[0].lower()
                    if type_str == "object" and self.entity_type == EntityType.OBJECT_PROP:
                        return True
                    if type_str == "landmark" and self.entity_type == EntityType.LANDMARK:
                        return True
            except (AttributeError, ValueError):
                pass
        
        return False

    def get_formatted_tag(self) -> str:
        """Get the formatted template tag string."""
        return f"{{{self.entity_type.value}:{self.tag}}}"


class Scene:
    name: str
    description: str
    template: str
    entities: list[BaseSceneEntity]
    template_tags: list[SceneTemplateTag]

    def __init__(self, name: str, description: str, template: str):
        self.name = name
        self.description = description
        self.template = template

    def __post_init__(self):
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

    def add_entity_by_tag(self, entity: BaseSceneEntity, template_tag: str):
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
    
    def __str__(self):
        return f"Scene: {self.name}\nDescription: {self.description}\nTemplate: {self.template}\nEntities: {self.entities}"
