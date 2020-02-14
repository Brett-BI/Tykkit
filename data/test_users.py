from app import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()


user1 = User(email="test@test.com", password=bcrypt.generate_password_hash("password"))
user2 = User(email="zdlr@ratm.rage", password=bcrypt.generate_password_hash("andTestify"))
user3 = User(email="johnnyB@yahoo.com", password=bcrypt.generate_password_hash("heyymamma"))
user4 = User(email="someEmail@email.com", password=bcrypt.generate_password_hash("secretsecret"))
user5 = User(email="h.p.love@horror.drd", password=bcrypt.generate_password_hash("cthuluRISES"))

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)

db.session.commit()

# exec(open('data/test_users.py').read())
# User.query.all()
