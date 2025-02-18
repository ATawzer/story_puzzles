from invoke import task
from story_puzzles.scene import Scene
from story_puzzles.db import init_db
from story_puzzles.entity_template import Character

@task
def test(c):
    init_db()
    template = """
    {character:John} is holding a(n) {object:Axe} next to {character:Jane}. There is a {landmark:Chopped Fallen Tree} behind them.
    """
    scene = Scene(
        name="Test Scene",
        description="Sample scene for testing",
        template=template
    ).save()
    print(scene.to_json())

@task
def add_character(c, name):
    Character(name=name).save()

@task
def add_object(c, name):
    ObjectProp(name=name).save()