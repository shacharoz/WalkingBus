from datetime import datetime, timedelta

from . import app, db, Child, Parent, Group, Progress

from flask import render_template, request, jsonify


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
                    if request.form.get(child.username):
                        group.current_trip().participants.append(child)
                db.session.commit()
        elif group.current_trip().progress == Progress.WALK_STARTED:
            if group.current_trip().walker.id == user.id:
                for participant in group.current_trip().participants:
                    if request.form.get(participant.username):
                        group.current_trip().passengers.append(participant)
                    else:
                        group.current_trip().passengers.remove(participant)
                if request.form.get('finish'):
                    group.current_trip().progress = Progress.WALK_FINISHED
                db.session.commit()
        elif group.current_trip().progress == Progress.WALK_FINISHED:
            pass
    return render_template('school_trip.html', user=user, group=group, Progress=Progress, children=children)


@app.route('/api/progress')
def api_progress():
    group = Group.query.first()
    return jsonify({ 'progress': group.current_trip().progress }), 200
