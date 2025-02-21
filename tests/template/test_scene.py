import pytest
from project_muse.template.scene import SceneTemplate, SceneTemplateSentence, SceneTemplateTag
from project_muse.types import EntityType
from project_muse.db import init_db

@pytest.fixture(autouse=True)
def setup_db():
    """Setup database connection before each test"""
    init_db()
    # Clean up any existing templates
    SceneTemplate.objects.delete()
    yield
    # Cleanup after tests
    SceneTemplate.objects.delete()

class TestSceneTemplateTag:
    def test_init(self):
        tag = SceneTemplateTag(EntityType.CHARACTER, "hero")
        assert tag.entity_type == EntityType.CHARACTER
        assert tag.tag_name == "hero"

    def test_str_representation(self):
        tag = SceneTemplateTag(EntityType.CHARACTER, "hero")
        assert str(tag) == "character:hero"
        assert repr(tag) == "character:hero"

class TestSceneTemplateSentence:
    def test_init(self):
        sentence = SceneTemplateSentence(text="Hello {character:hero}!", order=0)
        assert sentence.text == "Hello {character:hero}!"
        assert sentence.order == 0
        assert sentence._template_tags is None

    def test_parse_template_tags_single(self):
        sentence = SceneTemplateSentence(text="Hello {character:hero}!", order=0)
        tags = sentence.template_tags
        assert len(tags) == 1
        assert tags[0].entity_type == EntityType.CHARACTER
        assert tags[0].tag_name == "hero"

    def test_parse_template_tags_multiple(self):
        sentence = SceneTemplateSentence(
            text="The {character:hero} found a {object_prop:sword} near the {landmark:tree}",
            order=0
        )
        tags = sentence.template_tags
        assert len(tags) == 3
        assert [tag.entity_type for tag in tags] == [
            EntityType.CHARACTER,
            EntityType.OBJECT_PROP,
            EntityType.LANDMARK
        ]
        assert [tag.tag_name for tag in tags] == ["hero", "sword", "tree"]

    def test_parse_template_tags_invalid(self):
        sentence = SceneTemplateSentence(
            text="Invalid {tag} and {invalid:tag} but {character:hero} is valid",
            order=0
        )
        tags = sentence.template_tags
        assert len(tags) == 1
        assert tags[0].entity_type == EntityType.CHARACTER
        assert tags[0].tag_name == "hero"

    def test_parse_template_tags_empty(self):
        sentence = SceneTemplateSentence(text="Plain text with no tags", order=0)
        assert len(sentence.template_tags) == 0

    def test_parse_template_tags_unclosed_brace(self):
        sentence = SceneTemplateSentence(text="Unclosed {character:hero brace", order=0)
        assert len(sentence.template_tags) == 0

    def test_str_representation(self):
        sentence = SceneTemplateSentence(text="Hello {character:hero}!", order=0)
        assert str(sentence) == "Hello {character:hero}!"

class TestSceneTemplate:
    def test_init(self):
        template = SceneTemplate(name="Test Template")
        assert template.name == "Test Template"
        assert len(template.sentences) == 0

    def test_add_sentence(self):
        template = SceneTemplate(name="Test Template").save()
        template.add_sentence("Hello {character:hero}!")
        assert len(template.sentences) == 1
        assert template.sentences[0].text == "Hello {character:hero}!"
        assert template.sentences[0].order == 0

    def test_add_multiple_sentences(self):
        template = SceneTemplate(name="Test Template").save()
        template.add_sentence("First sentence")
        template.add_sentence("Second sentence")
        assert len(template.sentences) == 2
        assert [s.order for s in template.sentences] == [0, 1]

    def test_update_sentence(self):
        template = SceneTemplate(name="Test Template").save()
        template.add_sentence("Original text")
        template.update_sentence(0, "Updated text")
        assert template.sentences[0].text == "Updated text"

    def test_update_sentence_invalid_order(self):
        template = SceneTemplate(name="Test Template").save()
        with pytest.raises(IndexError):
            template.update_sentence(0, "Invalid update")

    def test_get_template_tags(self):
        template = SceneTemplate(name="Test Template").save()
        template.add_sentence("The {character:hero} found a {object_prop:sword}")
        template.add_sentence("Near the {landmark:tree}")
        
        tags = template.get_template_tags()
        assert len(tags) == 3
        assert [tag.tag_name for tag in tags] == ["hero", "sword", "tree"]

    def test_get_tags_by_sentence(self):
        template = SceneTemplate(name="Test Template").save()
        template.add_sentence("The {character:hero} found a {object_prop:sword}")
        template.add_sentence("Near the {landmark:tree}")
        
        tags_by_sentence = template.get_tags_by_sentence()
        assert len(tags_by_sentence) == 2
        assert len(tags_by_sentence[0]) == 2  # First sentence has 2 tags
        assert len(tags_by_sentence[1]) == 1  # Second sentence has 1 tag

    def test_str_representation(self):
        template = SceneTemplate(name="Test Template")
        assert str(template) == "Test Template"
        assert repr(template) == "Test Template"

    def test_persistence(self):
        # Test that templates are properly saved and retrieved from the database
        template = SceneTemplate(name="Persistence Test").save()
        template.add_sentence("Test sentence")
        
        # Retrieve from database
        retrieved = SceneTemplate.objects(name="Persistence Test").first()
        assert retrieved.name == "Persistence Test"
        assert len(retrieved.sentences) == 1
        assert retrieved.sentences[0].text == "Test sentence"

    def test_unique_template_names(self):
        # Test that template names must be unique
        SceneTemplate(name="Unique Test").save()
        with pytest.raises(Exception):  # MongoEngine will raise a NotUniqueError
            SceneTemplate(name="Unique Test").save() 