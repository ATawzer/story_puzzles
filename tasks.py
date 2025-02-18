from invoke import task
from story_puzzles.scene import Scene
from story_puzzles.db import init_db

@task
def test(c):
    init_db()
    template = """
    {character:Character 1} is holding a(n) {object:Axe} next to {character:Character 2}. There is a {landmark:Chopped Fallen Tree} behind them.
    """
    scene = Scene(
        name="Test Scene",
        description="Sample scene for testing",
        template=template
    ).save()
    print(scene.to_json())