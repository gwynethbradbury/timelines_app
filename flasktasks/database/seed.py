from flasktasks import db
from flasktasks.models import Tag, Storyline, Event, Color, CastmemberColor, Castmember, User, EventChar


def create_tags(uid):
    tag1 = Tag(user_id=uid,name="Work", color= Color.GREY)
    
    db.session.add(tag1)
    db.session.commit()

def create_storylines(uid):
    tags=Tag.query.all()

    storyline1 = Storyline(user_id=uid,title="Unnamed storyline", description='Misc.', tag_id= tags[0].id)

    db.session.add(storyline1)
    db.session.commit()

def create_events(uid):
    stories=Storyline.query.all()
    chars=Castmember.query.all()
    for i in range(len(stories)):
        event1 = Event(user_id=uid, title="First Event", description= "Some useful description", storyline_id= stories[i].id,castmember_id=chars[0].id)

        db.session.add(event1)
    db.session.commit()

def create_castmembers(uid):
    castmember0 = Castmember(user_id=uid,name="Unnamed",initials="U")
    db.session.add(castmember0)
    db.session.commit()

def create_user():
    u = User()
    db.session.add(u)
    db.session.commit()
    return u.id

def link_event_char(uid):
    c = Castmember.query.first()
    e = Event.query.first()
    ce = EventChar(c.id,e.id)
    db.session.add(ce)
    db.session.commit()




def run_seed():
    print("Creating default user")
    uid = create_user()
    create_defaults(uid)

def create_defaults(uid):
    print("Creating character...")
    create_castmembers(uid)

    print("Creating Tags...")
    create_tags(uid)

    print("Creating storylines...")
    create_storylines(uid)

    print("Creating events...")
    create_events(uid)

    print("Adding char to event ...")
    link_event_char(uid)

    return
