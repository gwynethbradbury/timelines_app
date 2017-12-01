from flasktasks import app, db
from flasktasks.models import LogEntry
from flasktasks.signals import event_created, storyline_created, castmember_created, chapter_created


@event_created.connect
def log_event_creation(event, **kwargs):
    message = "The event {} was created by u:{}." .format(event.title,event.user_id)
    log_entry(message,event.user_id)

@chapter_created.connect
def log_chapter_creation(chapter, **kwargs):
    message = "The chapter {} was created by u:{}." .format(chapter.title,chapter.user_id)
    log_entry(message,chapter.user_id)


@castmember_created.connect
def log_castmember_creation(castmember, **kwargs):
    message = "The character {} was created by u:{}." .format(castmember.name, castmember.user_id)
    log_entry(message,castmember.user_id)

@storyline_created.connect
def log_storyline_creation(storyline, **kwargs):
    message = "The storyline {} was created by u:{}." .format( storyline.title,storyline.user_id)
    log_entry(message,storyline.user_id)


def log_entry(message,uid):
    log_entry = LogEntry(message,uid)
    db.session.add(log_entry)
    db.session.commit()
