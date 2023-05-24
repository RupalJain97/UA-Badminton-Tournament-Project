from app import db

"""
Class Login stores Login information related to Users (Admin and Players)
"""


class Login(db.Model):
    __tablename__ = "login"
    login_id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    users = db.relationship('Users', backref='login', lazy=True)

    def __init__(self, login_id: str, password: str):
        self.login_id = login_id
        self.password = password

    def __repr__(self):
        return "<Login(login_id='%s', password='%s')>" % (self.login_id, self.password)
