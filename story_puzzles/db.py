from mongoengine import connect
from mongita import MongitaClient

def init_db():
    client = MongitaClient()  # Creates in-memory client
    # Connect to a named database instead of using index 0
    connect('story_puzzles_db', host='mongita://', alias='default') 