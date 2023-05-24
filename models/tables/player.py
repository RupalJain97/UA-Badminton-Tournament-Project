from app import db

"""
Class Player, stores information relation to badminton players
"""


class Player(db.Model):
    __tablename__ = "player"
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    social_media_consent = db.Column(db.Boolean, nullable=False)
    competing_gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    club_name = db.Column(db.String(30), nullable=True)

    def __init__(self, player_id: int, competing_gender: str, social_media_consent: bool = True,
                 phone_number: str = None, dob: str = None, club_name: str = None):
        """
        Constructor for Player Table
        :param player_id: Primary for the Player Table, FK references Users table
        :param social_media_consent: if True, player agrees for photography/videography
        :param competing_gender: Determines eligibility for playing in competing gender-specific matches
        :param phone_number: contact number
        :param dob: determines age
        :param club_name: the name of the club player belongs to
        """
        self.player_id = player_id
        self.social_media_consent = social_media_consent
        self.competing_gender = competing_gender
        self.phone_number = phone_number
        self.dob = dob
        self.club_name = club_name

    def __repr__(self):
        return "<Player(player_id='%s', competing_gender'%s')>" % (
            self.player_id, self.competing_gender)
