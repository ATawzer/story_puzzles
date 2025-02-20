from invoke import task
from story_puzzles.scene.template import SceneTemplate
from story_puzzles.db import init_db
from story_puzzles.entity.template import CharacterTemplate, ObjectPropTemplate, LandmarkTemplate, CreatureTemplate

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
def add_creature(c, name, description=""):
    """Add a new creature to the database"""
    init_db()
    creature = CreatureTemplate(name=name, description=description).save()
    print(f"Created creature: {creature.name}")

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
    if entity_type == 'creature':
        entities = CreatureTemplate.objects.all()
    elif entity_type == 'character':
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
        print("\nCreatures:")
        for entity in CreatureTemplate.objects.all():
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

@task
def export_db(c, output_file="db_backup.json"):
    """Export the entire database to a JSON file
    
    Args:
        output_file (str): Path to the output JSON file
    """
    init_db()
    import json
    from mongoengine.base import BaseDocument
    from bson import ObjectId
    from story_puzzles.scene.template import SceneTemplate
    from story_puzzles.entity.template import CharacterTemplate, ObjectPropTemplate, LandmarkTemplate

    class MongoEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            if isinstance(obj, BaseDocument):
                return obj.to_mongo()
            return json.JSONEncoder.default(self, obj)

    data = {
        'scene_templates': [template.to_mongo() for template in SceneTemplate.objects.all()],
        'characters': [char.to_mongo() for char in CharacterTemplate.objects.all()],
        'creatures': [creature.to_mongo() for creature in CreatureTemplate.objects.all()],
        'objects': [obj.to_mongo() for obj in ObjectPropTemplate.objects.all()],
        'landmarks': [landmark.to_mongo() for landmark in LandmarkTemplate.objects.all()]
    }

    with open(output_file, 'w') as f:
        json.dump(data, f, cls=MongoEncoder, indent=2)
    
    print(f"Database exported to {output_file}")

@task
def import_db(c, input_file="db_backup.json"):
    """Import database from a JSON file
    
    Args:
        input_file (str): Path to the input JSON file
    """
    init_db()
    import json
    from story_puzzles.scene.template import SceneTemplate
    from story_puzzles.entity.template import CharacterTemplate, ObjectPropTemplate, LandmarkTemplate

    # Clear existing data
    SceneTemplate.objects.delete()
    CharacterTemplate.objects.delete()
    ObjectPropTemplate.objects.delete()
    LandmarkTemplate.objects.delete()

    with open(input_file, 'r') as f:
        data = json.load(f)

    # Helper function to clean MongoDB-specific fields
    def clean_mongo_data(data):
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if not k.startswith('_')}
        return data

    # Import scene templates
    for template_data in data['scene_templates']:
        SceneTemplate(**clean_mongo_data(template_data)).save()

    # Import characters
    for char_data in data['characters']:
        CharacterTemplate(**clean_mongo_data(char_data)).save()

    # Import objects
    for obj_data in data['objects']:
        ObjectPropTemplate(**clean_mongo_data(obj_data)).save()

    # Import landmarks
    for landmark_data in data['landmarks']:
        LandmarkTemplate(**clean_mongo_data(landmark_data)).save()

    # Import creatures
    for creature_data in data.get('creatures', []):
        CreatureTemplate(**clean_mongo_data(creature_data)).save()

    print(f"Database imported from {input_file}")

