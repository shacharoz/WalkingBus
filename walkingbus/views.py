from datetime import datetime

from . import app, Parent, Group

from flask import render_template, jsonify

PROGRESS_AWAITING_WALKER = 0
PROGRESS_AWAITING_PARENT_CONFIMATION = 1
PROGRESS_WALKING_STARTED = 2
PROGRESS_WALK_FINISHED = 3


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/school-trip')
def school_trip():
    group = Group.query.first()
    
    #group.start_trip()
    return render_template('school_trip.html', user=Parent.query.first(), group=group)


@app.route('/start')
def start():
    return jsonify({ 'success': True })
