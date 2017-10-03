from flasktasks import app, db
from flasktasks.models import LogEntry
from flasktasks.signals import event_created, storyline_created, castmember_created


@event_created.connect
def log_event_creation(event, **kwargs):
    message = "The event \"%s\" was created." % event.title
    log_entry(message)


@castmember_created.connect
def log_castmember_creation(castmember, **kwargs):
    message = "The character \"%s\" was created." % castmember.name
    log_entry(message)

@storyline_created.connect
def log_storyline_creation(storyline, **kwargs):
    message = "The storyline \"%s\" was created." % storyline.title
    log_entry(message)


def log_entry(message):
    log_entry = LogEntry(message)
    db.session.add(log_entry)
    db.session.commit()
