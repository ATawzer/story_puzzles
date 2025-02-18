from mongoengine import connect

def init_db():
    connect('story_puzzles_db', host='mongodb://localhost:27017/story_puzzles_db', alias='default') 