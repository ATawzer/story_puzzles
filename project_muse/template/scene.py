from mongoengine import Document, StringField, ListField, EmbeddedDocumentField
from .entity import *

class SceneTemplateTag:

    def __init__(self, entity_type: EntityType, tag_name: str, sentence_num: int):
        self.entity_type = entity_type
        self.tag_name = tag_name
        self.sentence_num = sentence_num
    
    def __str__(self):
        return f"{self.entity_type.value}:{self.tag_name} (sentence {self.sentence_num})"
    
    def __repr__(self):
        return self.__str__()

    def is_valid_option(self, entity: 'BaseEntityTemplate') -> bool:
        """Check if the given entity is valid for this tag."""
        return entity.entity_type == self.entity_type

class SceneTemplate(Document):
    name = StringField(required=True)
    template_description = StringField(required=True)

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