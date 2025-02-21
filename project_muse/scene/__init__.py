from ..template.scene import SceneTemplate, SceneTemplateTag
from ..template.entity import BaseEntityTemplate

class SceneEntity:
    """ This is a scene instanced entity, it maps a template tag in a scene template
    to a BaseEntity that is filling it.
    """
    
    def __init__(self, entity: BaseEntityTemplate, template_tag: SceneTemplateTag):
        self.entity = entity
        self.template_tag = template_tag
class SceneTag:
    """
    Handles the relationship between an instance of a template tag in the scene template
    and an instance of an entity that fills it.
    """

    def __init__(self, scene_template_tag: SceneTemplateTag, scene_entity: SceneEntity):
        self.scene_template_tag = scene_template_tag
        self.scene_entity = scene_entity
    
    def __str__(self):
        return f"{self.entity_type.value}:{self.tag_name} (sentence {self.sentence_num})"
    
    def __repr__(self):
        return self.__str__()

    def is_valid_option(self, entity: 'BaseEntityTemplate') -> bool:
        """Check if the given entity is valid for this tag."""
        return entity.entity_type == self.entity_type
    
class Scene:
    """
    An instance of a scene. The player will be able to see this scene and fill
    in the template tags with entities.
    """

    def __init__(self, scene_template: SceneTemplate):
        self.scene_template = scene_template
        self.scene_tag_container = []

    def parse_template(self):
        """Parse the template and create the entities."""
        pass

    def create_entity_by_tag(self, tag: SceneTemplateTag, entity: BaseEntityTemplate):
        """Add an entity to the scene by its tag."""
        if tag.is_valid_option(entity) and not self.is_entity_in_scene(entity):
            self.entities.append(BaseSceneEntity(entity, tag))
        
    def is_entity_in_scene(self, entity: 'BaseEntityTemplate') -> bool:
        """Check if an entity is already in the scene."""
        return any(scene_entity.entity.name == entity.name for scene_entity in self.entities)

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
    
     def get_template_tags(self) -> list[SceneTemplateTag]:
        """Parse the template string and saves a list of SceneTemplateTag objects."""
        template_tags = []
        
        # Split into sentences
        sentences = self.template_description.split('.')
        
        for sentence_num, sentence in enumerate(sentences, 1):
            if not sentence.strip():
                continue
            
            current_pos = 0
            while True:
                # Find the next opening brace
                start = sentence.find('{', current_pos)
                if start == -1:
                    break
                
                # Find the corresponding closing brace
                end = sentence.find('}', start)
                if end == -1:
                    break
                
                # Extract the tag content
                tag_content = sentence[start + 1:end]
                
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
                    
                    template_tags.append(SceneTemplateTag(
                        entity_type, 
                        identifier.strip(),
                        sentence_num
                    ))
                    
                except ValueError:
                    # Skip malformed tags
                    pass
                
                current_pos = end + 1
        
        return template_tags

    def get_tags_by_sentence(self) -> dict[int, list[SceneTemplateTag]]:
        """Group template tags by sentence number."""
        tags_by_sentence = {}
        for tag in self.get_template_tags():
            if tag.sentence_num not in tags_by_sentence:
                tags_by_sentence[tag.sentence_num] = []
            tags_by_sentence[tag.sentence_num].append(tag)
        return tags_by_sentence

        
