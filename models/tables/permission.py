from app import db

"""
Class Permission: Stores rwx permissions for Admins and Players
"""


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    read = db.Column(db.Boolean, nullable=False)
    write = db.Column(db.Boolean, nullable=False)
    delete = db.Column(db.Boolean, nullable=True)
    user_permission = db.relationship('UserPermission', backref='permission', lazy=True)

    def __init__(self, read: bool, write: bool, delete: bool):
        """
        Constructor for Permission Table
        :param read: Data read permission
        :param write: Data write permission
        :param delete: Data delete permission
        """
        self.read = read
        self.write = write
        self.delete = delete

    def __repr__(self):
        return "<Permissions(id='%s', read='%s', write='%s', delete'%s')>" % (
            self.id, self.read, self.write, self.delete)
