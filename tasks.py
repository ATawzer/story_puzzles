from invoke import task
from story_puzzles.scene import Scene

@task
def test(c):
    template = """{structure:Cottage 1} and {structure:Cottage 2} are nestled on a hillside. 
    {character:Character 1} is tending with a(n) {object:Hoe} to a small garden of {labdmark:Field of Wheat}. 
    A {creature:Cow} {verb:grazes} in a pasture nearby. 
    {character:Character 2} is on the way to tend to the {creature:Cow} with a(n) {object:Milk Pale}. {character:Character 4},
    the owner of {structure:Cottage 1} is {verb:arguing} with {character:Character 3}, 
    the owner of {character:Cottage 2}. {character:Character 3} is holding a(n) {object:Axe}, 
    by {structure:Cottage 1} a {landmark:Chopped Fallen Tree}.
    """
    scene = Scene(template)
    print(scene)