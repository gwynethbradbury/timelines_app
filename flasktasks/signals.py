from blinker import Namespace


flasktasks_signals = Namespace()
chapter_created = flasktasks_signals.signal('chapter-created')
event_created = flasktasks_signals.signal('event-created')
castmember_created = flasktasks_signals.signal('castmember-created')
storyline_created = flasktasks_signals.signal('storyline-created')
