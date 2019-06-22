from datetime import datetime, timedelta

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
children_assoc = Table(
    'children_assoc',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('parent_id', Integer, ForeignKey('parent.id')),
)

# Creating association Table for groups and children. 
group_assoc = Table(
    'group_assoc',
    Column('child_id', Integer, ForeignKey('child.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)


class User(object):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    address = Column(String, nullable=False)


class Parent(User, Model):
    pass


class Child(User, Model):
    parents = relationship('Parent', secondary=children_assoc, backref=backref('children', lazy='dynamic'))
    groups = relationship('Group', secondary=group_assoc, backref=backref('children', lazy='dynamic'))


class School(Model):
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, unique=True)


class Group(Model):
    id = Column(Integer, primary_key=True)
    school = Column(Integer, ForeignKey('school.id'), nullable=False)
    name = Column(String, nullable=False, unique=False)
    owner = Column(Integer, ForeignKey('parent.id'), nullable=False)
