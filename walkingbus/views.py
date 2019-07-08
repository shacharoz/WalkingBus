from datetime import datetime

from . import app, db, Child, Parent, Group, Progress

from flask import render_template, jsonify


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/school-trip')
def school_trip():
    group = Group.query.first()
    user = Parent.query.first()
    children = Child.query.filter(Child.parents.contains(user) and Child.groups.contains(group)).all()
    # TODO: not final version, this is just a temporary workaround.
    # we should call 'Group.new_trip()' when a parent volunteers to be walker.
    if (not getattr(group, 'current_trip', None) or 
       getattr(group, 'current_trip', None).progress == Progress.WALK_FINISHED):
        group.new_trip(walker=user)
    return render_template('school_trip.html', user=user, group=group, Progress=Progress, children=children)


@app.route('/start')
def start():
    return jsonify({ 'success': True })
