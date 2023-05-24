from models.database import db
# noinspection PyUnresolvedReferences
from models.models import Permission  # do not delete

"""
Class User Permission stores Permission ID corresponding to User ID, This table forms a composite key between the two.
"""


class UserPermission(db.Model):
    __tablename__ = "user_permission"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

    def __init__(self, user_id, permission_id):
        """
        Constructor for UserPermission
        :param user_id: the ID of the user table
        :param permission_id: the permission ID this user is entitled to
        """
        self.user_id = user_id
        self.permission_id = permission_id

    def __repr__(self):
        return f"<UserPermission(user_id='{self.user_id}', permission_id='{self.permission_id}')>"
