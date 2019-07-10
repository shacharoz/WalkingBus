from datetime import datetime, timedelta
from enum import IntEnum

from walkingbus import db


Model = db.Model
Table = db.Table
Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime
ForeignKey = db.ForeignKey
backref = db.backref
relationship = db.relationship


# Creating association Table for parents and children.
child_assoc = Table(
    'child_assoc',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('parent_id', Integer, ForeignKey('parent.id')),
)

# Creating association Table for groups and children. 
group_assoc = Table(
    'group_assoc',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

#
trip_assoc = Table(
    'trip_assoc',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('trip_id', Integer, ForeignKey('trip.id')),
)

trip_assoc2 = Table(
    'trip_assoc2',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('trip_id', Integer, ForeignKey('trip.id')),
)


class Progress(object):

    AWAITING_WALKER = 0
    AWAITING_PARENT_CONFIMATION = 1
    WALK_STARTED = 2
    WALK_FINISHED = 3


class User(object):

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    address = Column(String, nullable=False)

class Parent(User, Model):

    trip = relationship('Trip', uselist=False, backref='walker')


class Child(User, Model):

    parents = relationship('Parent', secondary=child_assoc, backref=backref('children', lazy='dynamic'))
    groups = relationship('Group', secondary=group_assoc, backref=backref('children', lazy='dynamic'))


class School(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False, unique=True)
    groups = relationship('Group', backref='school')


class Group(Model):

    id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=False)
    name = Column(String, nullable=False, unique=False)
    trips = relationship('Trip', backref='group')
    owner = Column(Integer, ForeignKey('parent.id'), nullable=False)

    def new_trip(self, **kwargs):
        current_trip = Trip(**kwargs, group=self)
        db.session.add(current_trip)  # Saving the current trip to trip history
        db.session.commit()  # Forcing commit to write to database
    
    def current_trip(self):
        return self.trips[-1] if len(self.trips) > 0 else None


class Trip(Model):

    # Values written to database
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    participants = relationship('Child', secondary=trip_assoc, backref=backref('trips', lazy='dynamic'))
    passengers = relationship('Child', secondary=trip_assoc2, backref=backref('_trips', lazy='dynamic'))
    walker_id = Column(Integer, ForeignKey('parent.id'), nullable=False)
    progress = Column(Integer, nullable=False, default=Progress.AWAITING_WALKER)

    def start(self):
        self.start_time = datetime.utcnow()
        self.progress = Progress.AWAITING_PARENT_CONFIMATION
        db.session.commit()
