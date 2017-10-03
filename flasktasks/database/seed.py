from flasktasks import db
from flasktasks.models import Tag, Storyline, Event, Color, CastmemberColor, Castmember


def create_tags():
    tag1 = Tag("Work", Color.GREY)
    
    db.session.add(tag1)
    db.session.commit()

def create_storylines():
    storyline1 = Storyline("Unnamed storyline", 'Misc.', 1)

    db.session.add(storyline1)
    db.session.commit()

def create_events():
    stories=Storyline.query.all()
    chars=Castmember.query.all()
    for i in range(len(stories)):
        event1 = Event("First Event", "Some useful description", stories[i].id,chars[0].id)

        db.session.add(event1)
    db.session.commit()

def create_castmembers():
    castmember0 = Castmember("Unnamed","U")
    db.session.add(castmember0)
    db.session.commit()



def run_seed():

    print("Creating character...")
    create_castmembers()

    print("Creating Tags...")
    create_tags()

    print("Creating storylines...")
    create_storylines()

    print("Creating events...")
    create_events()
