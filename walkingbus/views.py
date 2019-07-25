from datetime import datetime, timedelta
from os import path

from . import app, db, login_manager, LoginForm, RegistrationForm, UpdateForm, bcrypt, Child, Parent, Group, Progress

from flask import render_template, request, jsonify, abort, redirect, flash
from flask_login import login_user, current_user, login_required
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(user_id):
    return Parent.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/school-trip/<int:id>', methods=['GET', 'POST'])
def school_trip(id):
    group = Group.query.first()
    user = Parent.query.filter_by(id=id).first()
    children = Child.query.filter(Child.parents.contains(user), Child.groups.contains(group)).all()
    # TODO: not final version, this is just a temporary workaround.
    # we should call 'Group.new_trip()' when a parent volunteers to be walker.
    if not group.current_trip() or (group.current_trip().progress == Progress.WALK_FINISHED and datetime.utcnow() - group.current_trip().start_time > timedelta(hours=12)):
        group.new_trip(walker_id=Parent.query.first().id)

    if request.method == 'POST':
        if group.current_trip().progress == Progress.AWAITING_WALKER:
            if group.current_trip().walker.id == user.id:
                group.current_trip().start()
        elif group.current_trip().progress == Progress.AWAITING_PARENT_CONFIMATION:
            if group.current_trip().walker.id == user.id:
                group.current_trip().progress = Progress.WALK_STARTED
                db.session.commit()
            else:
                for child in children:
                    if request.form.get(child.username) and (child not in group.current_trip().participants):
                        group.current_trip().participants.append(child)
                    elif not request.form.get(child.username) and child in group.current_trip().participants:
                        group.current_trip().participants.remove(child)
                db.session.commit()
        elif group.current_trip().progress == Progress.WALK_STARTED:
            if group.current_trip().walker.id == user.id:
                for participant in group.current_trip().participants:
                    if request.form.get(participant.username) and (participant not in group.current_trip().passengers):
                        group.current_trip().passengers.append(participant)
                    elif not request.form.get(participant.username) and participant in group.current_trip().passengers:
                        group.current_trip().passengers.remove(participant)
                if request.form.get('finish'):
                    group.current_trip().progress = Progress.WALK_FINISHED
                db.session.commit()
        elif group.current_trip().progress == Progress.WALK_FINISHED:
            pass
    return render_template('school_trip.html', user=user, group=group, Progress=Progress, children=children)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        parent = Parent(username=form.username.data, fullname=form.fullname.data, address=form.address.data, password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(parent)
        db.session.commit()
        login_user(parent)
        return redirect('/')
    return render_template('sign_up.html', form=form)


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = Parent.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            flash('Login successful.', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials, login failed!', 'danger')
    return render_template('sign_in.html', form=form)


@login_required
@app.route('/account', methods=['GET', 'POST'])
def account():
    groups = []
    for child in current_user.children:
        print(groups)
        groups.extend(child.groups)
    groups = set(groups)
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.address = form.address.data
        db.session.commit()
        if form.picture.data:
            f = form.picture.data
            filename = secure_filename(current_user.username)
            f.save(path.join('img', filename))
        flash('Your account has been updated!', 'success')
    return render_template('account.html', groups=groups, form=form)


@app.route('/api/progress')
def api_progress():
    group = Group.query.first()
    if group.current_trip():
        return jsonify({ 'progress': group.current_trip().progress }), 200
    else:
        return abort(404)
