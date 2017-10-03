from flasktasks import db
from enum import Enum
from time import strftime


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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    storyline_id = db.Column(db.Integer, db.ForeignKey('storyline.id'))
    castmember_id = db.Column(db.Integer, db.ForeignKey('castmember.id'))
    event_occurs_percent = db.Column(db.Float)

    def __init__(self, title, description, storyline_id, castmember_id, event_occurs_percent=0):
        self.title = title
        self.description = description
        self.status = Status.TO_DO.value
        self.storyline_id = storyline_id
        self.castmember_id = castmember_id
        self.event_occurs_percent = event_occurs_percent

class Storyline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(210))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    events = db.relationship('Event', backref='storyline', lazy='dynamic')

    def __init__(self, title, description, tag_id):
        self.title = title
        self.description = description
        self.tag_id = tag_id

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    color = db.Column(db.Integer)
    storylines = db.relationship('Storyline', backref='tag', lazy='dynamic')

    def __init__(self, name, color=Color.GREY):
        self.name = name
        self.color = color.value
    
    def style(self):
        color = Color(self.color)
        return "tagged tag-%s" % color.name.lower()

class Castmember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    initials = db.Column(db.String(3), unique=True)
    color = db.Column(db.Integer)
    events = db.relationship('Event', backref='castmember', lazy='dynamic')

    def __init__(self, name="Unassigned", initials="U", color=Color.GREY):
        self.name = name
        self.color = color.value
        self.initials = initials

    def style(self):
        color = CastmemberColor(self.color)
        return "tagged tag-%s" % color.name.lower()

    def bgcol(self):
        color = CastmemberColor(self.color)
        return "bg-%s" % color.name.lower()

# class EventChar(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
#
#     def __init(self,character_id,event_id):
#         self.character_id = character_id
#         self.event_id = event_id



class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(30))
    message = db.Column(db.String(140))

    def __init__(self, message):
        self.message = message
        self.timestamp = strftime("%d-%m-%Y %H:%M:%S")
