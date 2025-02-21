from mongoengine import Document, StringField, ListField, EmbeddedDocumentField, IntField, EmbeddedDocument
from ..types import EntityType

class SceneTemplateTag:
    """
    Represents an unfilled tag in a scene template that the user will fill in with an entity.
    """
    def __init__(self, entity_type: EntityType, tag_name: str):
        self.entity_type = entity_type
        self.tag_name = tag_name

    def __str__(self):
        return f"{self.entity_type.value}:{self.tag_name}"
    
    def __repr__(self):
        return self.__str__()

class SceneTemplateSentence(EmbeddedDocument):
    """
    Represents a sentence in a scene template. 

    Comprised of template tags that the user will fill in with an entity.
    """
    text = StringField(required=True)
    order = IntField(required=True)
    
    def __init__(self, *args, **kwargs):
        self._template_tags = None
        super().__init__(*args, **kwargs)
    
    @property
    def template_tags(self) -> list[SceneTemplateTag]:
        """Parse and cache template tags in the sentence."""
        if self._template_tags is None:
            self._template_tags = self._parse_template_tags()
        return self._template_tags

    def _parse_template_tags(self) -> list[SceneTemplateTag]:
        """Parse the template tags from the sentence string.
        
        tags are formatted as {entity_type:tag_name}
        """
        tags = []
        current_pos = 0
        
        while True:
            start = self.text.find('{', current_pos)
            if start == -1:
                break
                
            end = self.text.find('}', start)
            if end == -1:
                break
                
            tag_content = self.text[start + 1:end]
            try:
                entity_type_str, tag_name = tag_content.split(':')
                try:
                    entity_type = EntityType(entity_type_str)
                    tags.append(SceneTemplateTag(entity_type, tag_name))
                except ValueError:
                    # Invalid entity type
                    pass
            except ValueError:
                # Malformed tag
                pass
                
            current_pos = end + 1
            
        return tags

    def __str__(self):
        return self.text
    
    def __repr__(self):
        return f"{self.order}: {self.text}"
    
    def __iter__(self):
        return iter(self.template_tags)
    
    def __getitem__(self, index: int):
        return self.template_tags[index]

class SceneTemplate(Document):
    """
    Represents a full scene template and correlates with a level.

    Comprised of sentences that the user will fill in with an entity.
    """
    name = StringField(required=True)
    sentences = ListField(EmbeddedDocumentField(SceneTemplateSentence))

    # Public Methods
    def add_sentence(self, text: str):
        """Add a new sentence to the template."""
        order = len(self.sentences)
        sentence = SceneTemplateSentence(text=text, order=order)
        self.sentences.append(sentence)
        self.save()

    def update_sentence(self, order: int, text: str):
        """Update an existing sentence."""
        if order >= len(self.sentences):
            raise IndexError(f"Order {order} is out of bounds for scene template {self.name}")
        self.sentences[order].text = text
        self.save()

    def get_sentences(self) -> list[SceneTemplateSentence]:
        return self.sentences
    
    def get_full_template_description(self) -> str:
        return "\n".join([str(sentence) for sentence in self.sentences])
    
    def get_sentence_by_order(self, order: int) -> SceneTemplateSentence:
        return self.sentences[order]
    
    def get_template_tags(self) -> list[SceneTemplateTag]:
        """Get all template tags across all sentences."""
        return [tag for sentence in self.sentences for tag in sentence.template_tags]

    def get_tags_by_sentence(self) -> dict[int, list[SceneTemplateTag]]:
        """Group template tags by sentence order."""
        return {sentence.order: sentence.template_tags for sentence in self.sentences}

    # Internal Overrides
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        return iter(self.sentences)
