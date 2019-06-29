from walkingbus import *

db.session.rollback()
db.drop_all()
db.create_all()
parent1 = Parent(username='JohnDoe', password=bcrypt.generate_password_hash('123456789'), fullname='John Doe', address='Bologna something')
parent2 = Parent(username='JaneDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Jane Doe', address='Bologna something')
parent3 = Parent(username='RichardDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Richard Doe', address='Bologna something')
"""
db.session.add(parent1)
db.session.add(parent2)
db.session.add(parent3)
db.session.commit()

school1 = School(name='Galvani', address='Some stree with a school in Bologna')
group1 = Group(school=school1.id, name='Group #1', owner=parent3.id)
db.session.add(group1)
db.session.commit()

child1 = Child(username='JohnnyDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Johnny Doe')
child1.parents.append(parent1)
child1.parents.append(parent2)
child1.groups.append(group1)

db.session.add(child1)
db.session.commit()


 """