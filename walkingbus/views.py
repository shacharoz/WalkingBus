from datetime import datetime

from . import app, db, Child, Parent, Group, Progress

from flask import render_template, request, jsonify


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/school-trip', methods=['GET', 'POST'])
def school_trip():
    group = Group.query.first()
    user = Parent.query.first()
    children = Child.query.filter(Child.parents.contains(user), Child.groups.contains(group)).all()
    # TODO: not final version, this is just a temporary workaround.
    # we should call 'Group.new_trip()' when a parent volunteers to be walker.
    if (not group.current_trip() or group.current_trip().progress == Progress.WALK_FINISHED):
        group.new_trip(walker_id=user.id)

    if request.method == 'POST':
        print(group.current_trip().progress)
        if group.current_trip().progress == Progress.AWAITING_WALKER:
            if group.current_trip().walker.id == user.id:
                print('Start')
                group.current_trip().start()
        elif group.current_trip().progress == Progress.AWAITING_PARENT_CONFIMATION:
                # if group.current_trip().walker.id != user.id:
                
                for child in children:
                    if request.form.get(child.username):
                        group.current_trip().participants.append(child)
                print(group.current_trip().participants)
        elif group.current_trip().progress == Progress.WALK_STARTED:
            pass
        elif group.current_trip().progress == Progress.WALK_FINISHED:
            pass
    return render_template('school_trip.html', user=user, group=group, Progress=Progress, children=children)
