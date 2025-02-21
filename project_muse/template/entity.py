from mongoengine import Document, StringField, EnumField, ListField
from ..types import EntityType

class BaseEntityTemplate(Document):
    """These are meant to persist across scenes"""
    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['name'], 'unique': True}
        ]
    }
    name = StringField(required=True, unique=True)
    description = StringField(default="")
    entity_type = EnumField(EntityType, required=True)
    possible_states = ListField(StringField(), default=list)

    def __str__(self):
        return f"{self.entity_type.value}: {self.name}"