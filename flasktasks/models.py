from flasktasks import db
from flasktasks import bcrypt

from enum import Enum
from time import strftime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

import datetime



# class Event():
#     pass
# class Castmember():
#     pass

class Status(Enum):
    TO_DO = 1
    DOING = 2
    DONE = 3

class Color(Enum):
    GREY = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5

class CastmemberColor(Enum):
    GREY=1
    ORANGE=6
    YELLOW=7
    GREEN=8
    BLUE=9
    PURPLE=10
    DARKGREY=11


class EventChar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    castmember_id = db.Column(db.Integer, db.ForeignKey('castmember.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __init__(self,castmember_id,event_id):
        self.castmember_id = castmember_id
        self.event_id = event_id

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    storyline_id = db.Column(db.Integer, db.ForeignKey('storyline.id'))
    # castmember_id = db.Column(db.Integer, db.ForeignKey('castmember.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_occurs_percent = db.Column(db.Float)


    cast = relationship("Castmember",
                    secondary=EventChar.__table__,
                    backref="events")


    def __init__(self, user_id, title, description, storyline_id, castmember_id, event_occurs_percent=0):
        self.title = title
        self.description = description
        self.status = Status.TO_DO.value
        self.storyline_id = storyline_id
        self.castmember_id = castmember_id
        self.event_occurs_percent = event_occurs_percent
        self.user_id = user_id


class Storyline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.String(210))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    events = db.relationship('Event', backref='storyline', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, user_id, title, description, tag_id):
        self.title = title
        self.description = description
        self.tag_id = tag_id
        self.user_id = user_id

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    color = db.Column(db.Integer)
    storylines = db.relationship('Storyline', backref='tag', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, user_id, name, color=Color.GREY):
        self.name = name
        self.color = color.value
        self.user_id = user_id
    
    def style(self):
        color = Color(self.color)
        return "tagged tag-%s" % color.name.lower()

class Castmember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    initials = db.Column(db.String(3))
    color = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, user_id, name="Unassigned", initials="U", color=Color.GREY):
        self.name = name
        self.color = color.value
        self.initials = initials
        self.user_id = user_id

    def getEvents(self):
        Events=[]
        EventChars = EventChar.query.filter_by(castmember_id=self.id).all()
        for e in EventChars:
            Events.append(Event.query.filter_by(event_id=e.event_id).first())
        return Events


    def style(self):
        color = CastmemberColor(self.color)
        return "tagged tag-%s" % color.name.lower()

    def bgcol(self):
        color = CastmemberColor(self.color)
        return "bg-%s" % color.name.lower()



class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(30))
    message = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, message):
        self.message = message
        self.timestamp = strftime("%d-%m-%Y %H:%M:%S")
        self.user_id = 1



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('active', db.Boolean)

    def __init__(self, username="default", password="password", email="default"):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.datetime.utcnow()
        self.active = True


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        """True, as all users are active. unless theyve been deactivated"""
        return self.active

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True #self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


    def __repr__(self):
        return '<User %r>' % (self.username)