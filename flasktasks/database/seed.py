from flasktasks import db
from flasktasks.models import Tag, Storyline, Event, Color, CastmemberColor, Castmember, User, EventChar, Book, Chapter


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
    castmember0 = Castmember(user_id=uid,name="Red",initials="R")
    castmember1 = Castmember(user_id=uid,name="Grandmother",initials="G")
    castmember2 = Castmember(user_id=uid,name="Wolf",initials="W")
    castmember3 = Castmember(user_id=uid,name="Mother",initials="M")
    db.session.add(castmember0)
    db.session.add(castmember1)
    db.session.add(castmember2)
    db.session.add(castmember3)
    db.session.commit()

def create_user():
    u = User()
    db.session.add(u)
    db.session.commit()
    return u.id

# def link_event_char(uid):
#     c = Castmember.query.first()
#     e = Event.query.first()
#     ce = EventChar(c.id,e.id)
#     db.session.add(ce)
#     db.session.commit()

def create_book(uid):
    a = Book('Collected Fairytales','A collection',uid)
    db.session.add(a)
    db.session.commit()
    b = a.id
    print("Creating chapters...")
    create_chapters(uid,b)

def create_chapters(uid,bid):
    c = Chapter('Little Red Riding Hood','The Fairytale',uid,bid)

    db.session.add(c)
    db.session.commit()

    print("Creating events...")
    create_events(uid,c.id)

def create_events(uid,cid):
    content0="<p>Once upon a time, there was a little girl who lived in a village near the forest.  Whenever she went out, the little girl wore a red riding cloak, so everyone in the village called her Little Red Riding Hood." \
            "<p>One morning, Little Red Riding Hood asked her mother if she could go to visit her grandmother as it had been awhile since theyd seen each other." \
            "<p>Thats a good idea, her mother said.  So they packed a nice basket for Little Red Riding Hood to take to her grandmother."
    content1="<p>When the basket was ready, the little girl put on her red cloak and kissed her mother goodbye." \
            "<p>Remember, go straight to Grandmas house, her mother cautioned. Dont dawdle along the way and please dont talk to strangers!  The woods are dangerous." \
            "<p>Dont worry, mommy, said Little Red Riding Hood, Ill be careful."
    content2="<p>But when Little Red Riding Hood noticed some lovely flowers in the woods, she forgot her promise to her mother.  She picked a few, watched the butterflies flit about for awhile, listened to the frogs croaking and then picked a few more. " \
            "<p>Little Red Riding Hood was enjoying the warm summer day so much, that she didnt notice a dark shadow approaching out of the forest behind her..." \
            "<p>Suddenly, the wolf appeared beside her." \
            "<p>What are you doing out here, little girl? the wolf asked in a voice as friendly as he could muster." \
            "<p>Im on my way to see my Grandma who lives through the forest, near the brook,  Little Red Riding Hood replied." \
            "<p>Then she realized how late she was and quickly excused herself, rushing down the path to her Grandmas house. "
    content3="<p>The wolf, in the meantime, took a shortcut..." \
            "<p>The wolf, a little out of breath from running, arrived at Grandmas and knocked lightly at the door." \
            "<p>Oh thank goodness dear!  Come in, come in!  I was worried sick that something had happened to you in the forest, said Grandma thinking that the knock was her granddaughter." \
            "<p>The wolf let himself in.  Poor Granny did not have time to say another word, before the wolf gobbled her up!" \
            "<p>The wolf let out a satisfied burp, and then poked through Grannys wardrobe to find a nightgown that he liked.  He added a frilly sleeping cap, and for good measure, dabbed some of Grannys perfume behind his pointy ears."
    content4="<p>A few minutes later, Red Riding Hood knocked on the door.  The wolf jumped into bed and pulled the covers over his nose.  Who is it? he called in a cackly voice." \
            "<p>Its me, Little Red Riding Hood." \
            "<p>Oh how lovely!  Do come in, my dear, croaked the wolf." \
            "<p>When Little Red Riding Hood entered the little cottage, she could scarcely recognize her Grandmother." \
            "<p>Grandmother!  Your voice sounds so odd.  Is something the matter? she asked." \
            "<p>Oh, I just have touch of a cold, squeaked the wolf adding a cough at the end to prove the point." \
            "<p>But Grandmother!  What big ears you have, said Little Red Riding Hood as she edged closer to the bed." \
            "<p>The better to hear you with, my dear, replied the wolf." \
            "<p>But Grandmother!  What big eyes you have, said Little Red Riding Hood." \
            "<p>The better to see you with, my dear, replied the wolf." \
            "<p>But Grandmother!  What big teeth you have, said Little Red Riding Hood her voice quivering slightly." \
            "<p>The better to eat you with, my dear, roared the wolf and he leapt out of the bed and began to chase the little girl." \
            "<p>Almost too late, Little Red Riding Hood realized that the person in the bed was not her Grandmother, but a hungry wolf."
    content5="<p>She ran across the room and through the door, shouting, Help!  Wolf! as loudly as she could." \
            "<p>A woodsman who was chopping logs nearby heard her cry and ran towards the cottage as fast as he could." \
            "<p>He grabbed the wolf and made him spit out the poor Grandmother who was a bit frazzled by the whole experience, but still in one piece.Oh Grandma, I was so scared!  sobbed Little Red Riding Hood, Ill never speak to strangers or dawdle in the forest again." \
            "<p>There, there, child.  Youve learned an important lesson.  Thank goodness you shouted loud enough for this kind woodsman to hear you!" \
            "<p>The woodsman knocked out the wolf and carried him deep into the forest where he wouldnt bother people any longer."
    content6="<p>Little Red Riding Hood and her Grandmother had a nice lunch and a long chat."


    e = Event(uid,'-',content0,chapter_id=cid, event_occurs_percent=0)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content1,chapter_id=cid, event_occurs_percent=1)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content2,chapter_id=cid, event_occurs_percent=2)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content3,chapter_id=cid, event_occurs_percent=3)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content4,chapter_id=cid, event_occurs_percent=4)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content5,chapter_id=cid, event_occurs_percent=5)
    db.session.add(e)
    # db.session.commit()
    e = Event(uid,'-',content6,chapter_id=cid, event_occurs_percent=6)
    db.session.add(e)
    db.session.commit()


def run_seed():
    print("Creating default user")
    uid = create_user()
    create_defaults(uid)

def create_defaults(uid):
    print("Creating characters...")
    create_castmembers(uid)
    print("Creating book...")
    create_book(uid)

    print("Creating Tags...")
    create_tags(uid)

    print("Creating storylines...")
    create_storylines(uid)


    # print("Adding char to event ...")
    # link_event_char(uid)

    return
