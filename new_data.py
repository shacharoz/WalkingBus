from walkingbus import *
import sqlalchemy.util.langhelpers

db.session.rollback()
db.drop_all()
db.create_all()

parent1 = Parent(username='JohnDoe', password=bcrypt.generate_password_hash('123456789'), fullname='John Doe', address='Some street')
parent2 = Parent(username='JaneRoe', password=bcrypt.generate_password_hash('123456789'), fullname='Jane Roe', address='Some street')
parent3 = Parent(username='RichardDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Richard Doe', address='Some street')

db.session.add(parent1)
db.session.add(parent2)
db.session.add(parent3)
db.session.commit()

school1 = School(name='Galvani', address='Some street with a school')
db.session.add(school1)
db.session.commit()

group1 = Group(school=school1, name='Group #1', owner=parent3.id)
db.session.add(group1)
db.session.commit()

child1 = Child(username='JohnnyDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Johnny Doe', address=parent1.address)
child1.parents.append(parent1)
child1.groups.append(group1)
child2 = Child(username='JamieDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Jamie Doe', address=parent1.address)
child2.parents.append(parent1)
child2.groups.append(group1)
child3 = Child(username='RickRoe', password=bcrypt.generate_password_hash('123456789'), fullname='Rick Roe', address=parent2.address)
child3.parents.append(parent2)
child3.groups.append(group1)
child4 = Child(username='JimmyRoe', password=bcrypt.generate_password_hash('123456789'), fullname='Jimmy Roe', address=parent2.address)
child4.parents.append(parent2)
child4.groups.append(group1)
child5 = Child(username='ElizabethDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Elizabeth Doe', address=parent3.address)
child5.parents.append(parent3)
child5.groups.append(group1)
child6 = Child(username='RobertDoe', password=bcrypt.generate_password_hash('123456789'), fullname='Robert Doe', address=parent3.address)
child6.parents.append(parent3)
child6.groups.append(group1)

db.session.add(child1)
db.session.commit()
