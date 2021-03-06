from flask import render_template, request, redirect, url_for, abort, jsonify, flash
from collections import defaultdict
from flasktasks import app, db
from flasktasks.models import Storyline, Event, Status, Tag, Color, CastmemberColor, Castmember, LogEntry, EventChar, Chapter, Book
from flasktasks.signals import event_created, storyline_created, castmember_created, chapter_created, book_created
from flasktasks.models import purge_divs

from flask_login import current_user
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/storylines')
def storylines():
    storylines = Storyline.query.filter_by(user_id=current_user.id).all()
    return render_template('storyline/index.html', storylines=storylines)

@app.route('/books')
def books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('book/index.html', books=books)

@app.route('/books/new', methods=['POST', 'GET'])
def new_book():
    if request.method == 'POST':
        book = Book(user_id=current_user.id, title=request.form.get('title'),
                              synopsis=request.form.get('synopsis'))
        db.session.add(book)
        db.session.commit()
        book_created.send(book)
        return redirect(url_for('books'))
    else:
        tags = Tag.query.filter_by(user_id=current_user.id).all()
        return render_template('book/new.html', tags=tags)

@app.route('/storylines/new', methods=['POST', 'GET'])
def new_storyline():
    if request.method == 'POST':
        storyline = Storyline(user_id=current_user.id, title=request.form.get('title'),
                              description=request.form.get('description'),
                              tag_id= request.form.get('tag_id'))
        db.session.add(storyline)
        db.session.commit()
        storyline_created.send(storyline)
        return redirect(url_for('storylines'))
    else:
        tags = Tag.query.filter_by(user_id=current_user.id).all()
        return render_template('storyline/new.html', tags=tags)

@app.route('/chapters', methods=['POST', 'GET'])
def chapters():
    chapters = Chapter.query.filter_by(user_id=current_user.id).all()
    return render_template('chapter/index.html',chapters=chapters)

@app.route('/reorder_book_chapters/<book_id>', methods=['POST', 'GET'])
def reorder_book_chapters(book_id):
    if request.method == 'POST':
        names = request.form.getlist('handles[]')
        new_num=0
        for n in names:
            chapter = Chapter.query.get_or_404(int(n))

            chapter.number = new_num
            new_num=new_num+1

            db.session.add(chapter)
        db.session.commit()


    return redirect('book/{}'.format(book_id))

@app.route('/reorder_chapter_events/<chapter_id>', methods=['POST', 'GET'])
def reorder_chapter_events(chapter_id):
    if request.method == 'POST':

        names = request.form.getlist('handles[]')
        new_num=0
        for n in names:
            event = Event.query.get_or_404(int(n))

            event.event_occurs_percent = new_num
            new_num=new_num+1

            db.session.add(event)
        db.session.commit()


    return redirect('chapters/{}'.format(chapter_id))

@app.route('/events', methods=['POST', 'GET'])
def events():

    if request.method == 'POST':
    #     import json
    #
    #     myJson = json.loads('sortables')
    #
    #     param3b1 = myJson['abo']['param3'][1]['param3b1']
    #
        names = request.form.getlist('handles[]')
        pass


    storyline = None
    castmember = None
    book=None
    if request.args.get('storyline_id'):
        storyline = Storyline.query.get_or_404(request.args.get('storyline_id'))
        if not storyline.user_id==current_user.id:
            abort(404)
        events = Event.query.filter_by(storyline_id=storyline.id,user_id=current_user.id).order_by(Event.event_occurs_percent.asc()).all()
    elif request.args.get('castmember_id'):
        castmember = Castmember.query.get_or_404(request.args.get('castmember_id'))
        if not castmember.user_id==current_user.id:
            abort(404)
        events = castmember.events#Event.query.filter_by(castmember_id=castmember.id,user_id=current_user.id).order_by(Event.event_occurs_percent.asc()).all()
    elif request.args.get('book_id'):
        book = Book.query.get_or_404(request.args.get('book_id'))
        if not book.user_id==current_user.id:
            abort(404)
        chapters = Chapter.query.filter_by(book_id=book.id,user_id=current_user.id).order_by(Chapter.id.asc()).all()
        events=[]
        for c in chapters:
            for e in c.events:
                events.append(e)
    else:
        events = Event.query.filter_by(user_id=current_user.id).order_by(Event.event_occurs_percent.asc()).all()

    events_by_status = defaultdict(list)
    for event in events:
        status = Status(event.status).name
        events_by_status[status].append(event)
    return render_template('event/index.html', events=events_by_status, events_by_time=events,
                           storyline=storyline,castmember=castmember, book=book)

@app.route('/castmembers')
def castmembers():
    # storyline = None
    # if request.args.get('storyline_id'):
    #     storyline = Storyline.query.get_or_404(request.args.get('storyline_id'))
    #     tasks = Task.query.filter_by(storyline_id=storyline.id).all()
    # else:
    #     tasks = Task.query.all()
    #
    # tasks_by_status = defaultdict(list)
    # for task in tasks:
    #     status = Status(task.status).name
    #     tasks_by_status[status].append(task)
    castmembers = Castmember.query.filter_by(user_id=current_user.id).all()
    # events=Event.query.filter_by(user_id=current_user.id).all()


    storyline = None
    castmember = None
    if request.args.get('storyline_id'):
        storyline = Storyline.query.get_or_404(request.args.get('storyline_id'))
        if not storyline.user_id==current_user.id:
            abort(404)
        events = Event.query.filter_by(storyline_id=storyline.id,user_id=current_user.id).all()
    elif request.args.get('castmember_id'):
        castmember = Castmember.query.get_or_404(request.args.get('castmember_id'))
        if not castmember.user_id==current_user.id:
            abort(404)
        events = Event.query.filter_by(castmember_id=castmember.id,user_id=current_user.id).all()
    else:
        events = Event.query.filter_by(user_id=current_user.id).all()

    # events_by_castmember = defaultdict(list)
    # for event in events:
    #     castmember = event.castmember.id
    #     events_by_castmember[str(castmember)].append(event)
    events.sort(key=lambda x: x.event_occurs_percent)
    return render_template('castmember/index.html', castmembers=castmembers, events=events)

@app.route('/castmembers/new', methods=['POST', 'GET'])
def new_castmember():

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(30), unique=True)
    # initials = db.Column(db.String(3), unique=True)
    # color = db.Column(db.Integer)
    # events = db.relationship('Event', backref='castmember', lazy='dynamic')
    if request.method == 'POST':
        color = CastmemberColor(int(request.form.get('color_id')))

        castmember = Castmember(user_id=current_user.id, name=request.form.get('name'),
                              initials=request.form.get('initials'),
                                color=color)
        db.session.add(castmember)
        db.session.commit()
        castmember_created.send(castmember)
        return redirect('/castmembers')
        # return redirect('/castmembers?castmember_id={}'.format(request.form.get('castmember_id')))
    else:
        storylines = Storyline.query.filter_by(user_id=current_user.id).all()
        castmembers = Castmember.query.filter_by(user_id=current_user.id).all()
        colors = { color.name: color.value for color in CastmemberColor }
        return render_template('castmember/new.html', storylines=storylines, castmembers = castmembers, colors=colors)

@app.route('/chapters/new', methods=['POST', 'GET'])
def new_chapter():
    books = Book.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        # if request.form.get('occurs_percent'):
        #     occurs_percent=request.form.get('occurs_percent')
        # else:
        #     occurs_percent=0
        chapter = Chapter(user_id=current_user.id, title=request.form.get('title'),
                           synopsis=request.form.get('synopsis'), book_id=request.form.get('book_id'))
        db.session.add(chapter)
        db.session.commit()
        chapter_created.send(chapter)
        return redirect('/chapters')
    else:
        return render_template('chapter/new.html', books=books)

@app.route('/events/new', methods=['POST', 'GET'])
def new_event():
    if request.method == 'POST':
        if request.form.get('occurs_percent'):
            occurs_percent=request.form.get('occurs_percent')
        else:
            occurs_percent=0
        event = Event(user_id=current_user.id, title=request.form.get('title'),
                    description=purge_divs(request.form.get('description')),
                    storyline_id=request.form.get('storyline_id'),
                    castmember_id=request.form.get('castmember_id'),
                    chapter_id=request.form.get('chapter_id'),
                      event_occurs_percent=occurs_percent)
        db.session.add(event)
        db.session.commit()
        event_created.send(event)
        if not request.form.get('chapter_id')=='-1':
            return redirect(url_for('chapter', chapter_id=request.form.get('chapter_id')))
        # if not request.form.get('storyline_id')=='-1':
        #     return redirect('/events?storyline_id={}'.format(request.form.get('storyline_id')))
        # if not request.form.get('castmember_id')=='-1':
        #     return redirect('/events?castmember_id={}'.format(request.form.get('castmember_id')))
        return redirect('/events')
    else:
        storylines = Storyline.query.filter_by(user_id=current_user.id).all()
        castmembers = Castmember.query.filter_by(user_id=current_user.id).all()
        chapters = Chapter.query.filter_by(user_id=current_user.id).all()
        return render_template('event/new.html', storylines=storylines, castmembers = castmembers, chapters=chapters)

@app.route('/chapters/<int:chapter_id>')
def chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if not chapter.user_id == current_user.id:
        abort(404)

    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('chapter/chapter.html', chapter=chapter, books=books)

@app.route('/chapters/<int:chapter_id>/edit', methods=['POST', 'GET'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    if not chapter.user_id == current_user.id:
        abort(404)

    if request.method == 'POST':
        try:
            chapter.title = request.form.get('title')
            chapter.synopsis = request.form.get('synopsis')
            chapter.book_id = request.form.get('book_id')
        except KeyError:
            abort(400)

        db.session.add(chapter)
        db.session.commit()
        flash("Saved",category='message')

        return redirect(url_for('chapter',chapter_id=chapter_id))
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('chapter/edit.html', chapter=chapter, books=books)


@app.route('/events/<int:event_id>', methods=['GET','POST'])
def event(event_id):
    event = Event.query.get_or_404(event_id)
    if not event.user_id == current_user.id:
        abort(404)

    if request.method == 'POST':
        event = Event.query.get_or_404(event_id)
        chapter_id = event.chapter_id
        if not event.user_id == current_user.id:
            abort(404)
        db.session.delete(event)
        db.session.commit()
        if chapter_id>0:
            return redirect('/chapters/{}'.format(chapter_id))
        return redirect('/events')

    castmembers = Castmember.query.filter_by(user_id=current_user.id).all()
    storylines = Storyline.query.filter_by(user_id=current_user.id).all()
    chapters = Chapter.query.filter_by(user_id=current_user.id).all()



    return render_template('event/event.html', event=event, castmembers=castmembers, storylines=storylines,chapters=chapters)

@app.route('/events/<int:event_id>/edit', methods=['POST', 'GET'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not event.user_id == current_user.id:
        abort(404)
    castmembers = Castmember.query.filter_by(user_id=current_user.id).all()
    storylines = Storyline.query.filter_by(user_id=current_user.id).all()
    chapters = Chapter.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        try:
            event.title = request.form.get('title')
            event.description = purge_divs(request.form.get('description'))
            # event.storyline_id = request.form.get('storyline_id')
            if not request.form.get('chapter_id')=='-1':
                event.chapter_id = request.form.get('chapter_id')
            # event.event_occurs_percent = request.form.get('occurs_percent')
        except KeyError:
            abort(400)

        db.session.add(event)
        db.session.commit()
        flash("Saved",category='message')
        return redirect(url_for('event',event_id=event.id))

    return render_template('event/edit.html', event=event, castmembers=castmembers, storylines=storylines,chapters=chapters)


@app.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.user_id == current_user.id:
        abort(404)

    return render_template('book/book.html', book=book)

@app.route('/book/<int:book_id>/edit', methods=['POST', 'GET'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.user_id == current_user.id:
        abort(404)


    if request.method == 'POST':
        try:
            book.title = request.form.get('title')
            book.synopsis= purge_divs(request.form.get('synopsis'))
        except KeyError:
            abort(400)

        db.session.add(book)
        db.session.commit()
        flash("Saved",category='message')
        return redirect(url_for('book',book_id=book_id))

    return render_template('book/edit.html', book=book)



@app.route('/events/<int:event_id>/set_status/<status>')
def set_status(event_id, status):
    event = Event.query.get_or_404(event_id)
    if not event.user_id == current_user.id:
        abort(404)
    try:
        event.status = Status[status.upper()].value
    except KeyError:
        abort(400)

    db.session.add(event)
    db.session.commit()
    return redirect(url_for('events'))

# region SET OWNER


@app.route('/events/<int:event_id>/set_castmember/<cast_id>')
def set_castmember(event_id, cast_id):
    event = Event.query.get_or_404(event_id)
    if not event.user_id == current_user.id:
        abort(404)
    try:
        eventchars_count = EventChar.query.filter_by(castmember_id=cast_id, event_id=event_id).count()
        if eventchars_count>0:
            ECList = EventChar.query.filter_by(castmember_id=cast_id, event_id=event_id).all()
            for e in ECList:
                db.session.delete(e)
        else:
            EC = EventChar(castmember_id=cast_id,event_id=event_id)
            db.session.add(EC)
    except KeyError:
        abort(400)

    db.session.commit()
    return redirect('/events/{}'.format(event_id))

# endregion

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    chapter_id = event.chapter_id
    if not event.user_id == current_user.id:
        abort(404)
    db.session.delete(event)
    db.session.commit()
    if chapter_id>0:
        return redirect('/chapters/{}'.format(chapter_id))
    return redirect('/events')

@app.route('/events/<int:event_id>')
def unassign_castmember(event_id):
    event = Event.query.get_or_404(event_id)
    if not event.user_id == current_user.id:
        abort(404)
    try:
        castmember = Event.query.filter_by(initials="U",user_id=current_user.id).all()
        if len(castmember)==0: abort(404)
        event.castmember_id = castmember[0].id
    except KeyError:
        abort(400)

    db.session.add(event)
    db.session.commit()
    return redirect('/events/{}'.format(event_id))
    
@app.route('/storylines/<int:storyline_id>', methods=['DELETE'])
def delete_storyline(storyline_id):
    storyline = Storyline.query.get_or_404(storyline_id)
    if not storyline.user_id == current_user.id:
        abort(404)
    db.session.delete(storyline)
    db.session.commit()
    return url_for('storylines')

@app.route('/tags/new', methods=['POST', 'GET'])
def new_tag():
    if request.method == 'POST':
        try:
            color = Color(int(request.form.get('color_id')))
        except ValueError:
            abort(400)
        tag = Tag(user_id=current_user.id, name=request.form.get('name'),color= color)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('storylines'))
    else:
        colors = { color.name: color.value for color in Color }
        return render_template('tags/new.html', colors=colors)


@app.route('/reader/<book_id>')
def reader(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.user_id == current_user.id:
        abort(404)
    return render_template('book/reader.html', book=book)

@app.route('/log')
def log():
    log_entries = LogEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('log.html', log_entries=log_entries)



# SECURITY

from forms import EmailPasswordForm
from util.security import ts
from util.email import send_email
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UsernamePasswordForm, EmailForm, PasswordForm, ChangePasswordForm

# from flask.ext.login import login_user , logout_user , current_user , login_required

@app.route('/accounts/create', methods=["GET", "POST"])
def create_account():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User( username=form.email.data,
            password = form.password.data,
            email = form.email.data
        )
        db.session.add(user)
        db.session.commit()
        uid = user.id

        defaultuser = User.query.filter_by(email='default').first_or_404()
        books = Book.query.filter_all(user_id=defaultuser.id).all()

        for b in books:
            bc = Book(b.title,b.synopsis,uid)
            db.session.add(bc)
            db.session.commit()

            for c in b.chapters:
                cc=Chapter(c.title,c.synopsis,uid,bc.id)
                db.session.add(cc)
                db.session.commit()

                for e in c.events:
                    ec=Event(uid,e.title,e.description,'-1','-1',cc.id,e.event_occurs_percent)
                    db.session.add(ec)
                db.session.commit()

        # Now we'll send the email confirmation link
        subject = "Confirm your email"

        token = ts.dumps(self.email, salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url)

        # We'll assume that send_email has been defined in myapp/util.py
        send_email(user.email, subject, html)

        return redirect(url_for("index"))

    return render_template("accounts/create.html", form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('signin'))


from database.seed import create_defaults


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = EmailPasswordForm()
    form2 = UsernamePasswordForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            uid=user.id
            defaultuser = User.query.filter_by(email='default').first_or_404()
            books = Book.query.filter_by(user_id=defaultuser.id).all()

            for b in books:
                bc = Book(b.title, b.synopsis, uid)
                db.session.add(bc)
                db.session.commit()

                for c in b.chapters:
                    cc = Chapter(c.title, c.synopsis, uid, bc.id)
                    db.session.add(cc)
                    db.session.commit()

                    for e in c.events:
                        ec = Event(uid, e.title, e.description, '-1', '-1', cc.id, e.event_occurs_percent)
                        db.session.add(ec)
                    db.session.commit()

            # SEND CONFIRMATION EMAIL
            subject = "Account created at {}.".format("Timelines")

            # Here we use the URLSafeTimedSerializer we created in `util` at the
            # beginning of the chapter
            token = ts.dumps(user.email, salt='recover-key')

            recover_url = url_for(
                'reset_with_token',
                token=token,
                _external=True)

            html = render_template(
                'email/create_account.html')

            # Let's assume that send_email was defined in myapp/util.py
            send_email(user.email, subject, html)
            flash('Email sent to: {}'.format(user.email))



            login_user(user, force=True)
            return redirect(url_for('index'))

    return render_template('signup.html', form=form, form2=form2)

@app.route('/signin', methods=["GET", "POST"])
def signin():
    form = EmailPasswordForm()
    form2 = UsernamePasswordForm()


    if request.method == 'POST':
        # pass
        try:
            if form2.validate_on_submit():
                user = User.query.filter_by(username=form2.username.data).first_or_404()
                if user is None:
                    flash('Username or Password is invalid', 'error')
                    return redirect(url_for('login'))

                if user.is_correct_password(form2.password.data):
                    login_user(user, force=True)
                    flash('Logged in successfully')
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('signup'))

        except Exception as e:
            pass

    return render_template('signup.html', form=form, form2=form2)



@app.route('/signout')
def signout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', books=books)

@app.route('/settings', methods=["GET", "POST"])
def settings():
    form=ChangePasswordForm()
    user = User.query.filter_by(id=current_user.id).first_or_404()

    if form.validate_on_submit():
        if form.password.data==form.repeatpassword.data:
            user.password=(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))


    return render_template('settings.html', form=form)

@app.route('/deleteaccount', methods=["GET","POST"])
def delete_account():
    user = User.query.filter_by(id=current_user.id).first_or_404()

    if request.method == 'POST':

        events=Event.query.filter_by(user_id=current_user.id).all()
        for e in events:
            db.session.delete(e)
        chapters=Chapter.query.filter_by(user_id=current_user.id).all()
        for e in chapters:
            ECs = EventChar.query.filter_by(event_id=e.id).all()
            for ec in ECs:
                db.session.delete(ec)
            db.session.delete(e)
        books=Book.query.filter_by(user_id=current_user.id).all()
        for e in books:
            db.session.delete(e)
        storylines=Storyline.query.filter_by(user_id=current_user.id).all()
        for e in storylines:
            db.session.delete(e)
        tags=Tag.query.filter_by(user_id=current_user.id).all()
        for e in tags:
            db.session.delete(e)
        cast=Castmember.query.filter_by(user_id=current_user.id).all()
        for e in cast:
            db.session.delete(e)
        log=LogEntry.query.filter_by(user_id=current_user.id).all()
        for e in log:
            db.session.delete(e)


        logout_user()
        db.session.delete(user)

        db.session.commit()

        return redirect(url_for("index"))


    return render_template('deleteaccount.html')

@app.route('/reset', methods=["GET", "POST"])
def reset():
    logout_user()

    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        # Let's assume that send_email was defined in myapp/util.py
        send_email(user.email, subject, html)
        flash('Email sent to: {}'.format(user.email))
        return redirect(url_for('index'))
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):

    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not form.password.data==form.repeatpassword.data:
            flash("Passwords don't match!")
        else:
            user = User.query.filter_by(email=email).first_or_404()

            user.password = form.password.data

            db.session.add(user)
            db.session.commit()

            login_user(user, force=True)
            flash("Password changed!")
            return redirect(url_for('index'))

    return render_template('reset_with_token.html', form=form, token=token)

