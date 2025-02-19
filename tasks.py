from invoke import task
from story_puzzles.scene.template import SceneTemplate
from story_puzzles.db import init_db
from story_puzzles.entity.template import CharacterTemplate, ObjectPropTemplate, LandmarkTemplate

@task
def init(c):
    """Initialize the database connection"""
    init_db()

@task
def add_scene_template(c, name, template):
    """Add a new scene template to the database
    
    Example:
        invoke add-scene-template --name "Forest Scene" \
            --description "A scene in the forest" \
            --template "{character:Hero} stands near a {landmark:Ancient Tree} holding a {object:Sword}"
    """
    init_db()
    scene_template = SceneTemplate(
        name=name,
        template_description=template,
    ).save()
    print(f"Created scene template: {scene_template.name}")

@task
def add_character(c, name, description=""):
    """Add a new character template to the database"""
    init_db()
    character = CharacterTemplate(name=name, description=description).save()
    print(f"Created character: {character.name}")

@task
def add_object(c, name, description=""):
    """Add a new object prop to the database"""
    init_db()
    obj = ObjectPropTemplate(name=name, description=description).save()
    print(f"Created object: {obj.name}")

@task
def add_landmark(c, name, description=""):
    """Add a new landmark to the database"""
    init_db()
    landmark = LandmarkTemplate(name=name, description=description).save()
    print(f"Created landmark: {landmark.name}")

@task
def list_templates(c):
    """List all scene templates in the database"""
    init_db()
    templates = SceneTemplate.objects.all()
    for template in templates:
        print(f"\nTemplate: {template.name}")
        print(f"Description: {template.template_description}")
        print(f"Template: {template.template}")

@task
def list_entities(c, entity_type=None):
    """List all entities in the database, optionally filtered by type"""
    init_db()
    if entity_type == 'character':
        entities = CharacterTemplate.objects.all()
    elif entity_type == 'object':
        entities = ObjectPropTemplate.objects.all()
    elif entity_type == 'landmark':
        entities = LandmarkTemplate.objects.all()
    else:
        # List all entities
        print("\nCharacters:")
        for entity in CharacterTemplate.objects.all():
            print(f"- {entity.name}: {entity.description}")
        print("\nObjects:")
        for entity in ObjectPropTemplate.objects.all():
            print(f"- {entity.name}: {entity.description}")
        print("\nLandmarks:")
        for entity in LandmarkTemplate.objects.all():
            print(f"- {entity.name}: {entity.description}")
        return

    for entity in entities:
        print(f"- {entity.name}: {entity.description}")

@task
def game(c):
    """Run the game"""
    init_db()
    c.run("streamlit run app.py")

@task
def editor(c):
    """Run the editor"""
    init_db()
    c.run("streamlit run editor.py")

