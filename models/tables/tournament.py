from app import db
from datetime import datetime

"""
Class Tournament, stores information relation to Tournament
"""


class Tournament(db.Model):
    __tablename__ = "tournament"
    tournament_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    registration_open = db.Column(db.Date, default=datetime.utcnow())
    registration_closed = db.Column(db.Date, default=datetime.utcnow())
    tournament_start_date = db.Column(db.Date, default=datetime.utcnow())
    tournament_end_date = db.Column(db.Date, default=datetime.utcnow())
    announcement = db.Column(db.String(400), nullable=True)

    def __init__(self, tournament_name: str, location: str, registration_open: str, registration_closed: str,
                 tournament_start_date: str, tournament_end_date: str, announcement: str = "") -> None:
        """
        Initialize a Tournament object with the given attributes.
        tournament_name: The name of the tournament.
        location: The location of the tournament.
        registration_open: The date (in MM-DD-YYYY format) when registration opens for the tournament.
        registration_closed: The date (in MM-DD-YYYY format) when registration closes for the tournament.
        tournament_start_date: The date (in MM-DD-YYYY format) when the tournament starts.
        tournament_end_date: The date (in MM-DD-YYYY format) when the tournament ends.
        announcement: announcement related to the tournament
        """
        # check if it has id cos player is using id.
        self.tournament_name = tournament_name
        self.location = location
        self.registration_open = registration_open
        self.registration_closed = registration_closed
        self.tournament_start_date = tournament_start_date
        self.tournament_end_date = tournament_end_date
        self.announcement = announcement
        matches = db.relationship("Match", backref="tournament", lazy=True)

    def __repr__(self) -> str:
        """Return a string representation of the Tournament object."""
        return f"<Tournament Tournament Name={self.tournament_name}, Location={self.location}, " \
               f"Registration Open Date={self.registration_open} - Registration Open Date={self.registration_closed}," \
               f"Tournament Start Date={self.tournament_start_date} - Tournament End Date={self.tournament_end_date}, " \
               f"Announcements={self.announcement}>"
