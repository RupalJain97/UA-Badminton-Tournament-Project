from app import db

"""
Class Event, stores information related to an event such as "U15", "WomenSingles", "WomenDoubles"
"""


class Event(db.Model):
    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(50))
    gender_allowed = db.Column(db.String(10), nullable=True)
    draw_set = db.Column(db.Boolean, default=False)
    max_participants_allowed = db.Column(db.Integer, nullable=True)
    matches = db.relationship("Match", backref="event", lazy=True)
    players_event_seeds = db.relationship('PlayersEventSeed', backref='event', lazy=True)
    # establishing the relationship in the Event class creates a connection between PlayersEventSeed and Event table
    # that can be used later when the PlayersEventSeed rows are added.

    def __init__(self, event_name: str, gender_allowed: str = None, max_participants_allowed: int = None) -> None:
        """
        Initialize an Event object with the given attributes.
        event_name: The name of the event.
        gender_allowed: The gender allowed to participate in the event (optional).
        max_participants_allowed: The maximum number of participants allowed in the event (optional).
        """
        self.event_name = event_name
        self.gender_allowed = gender_allowed
        self.max_participants_allowed = max_participants_allowed

    def __repr__(self) -> str:
        """Return a string representation of the Event object."""
        return f"<Event Name={self.event_name}, Gender allowed={self.gender_allowed}," \
               f"Max participants Allowed={self.max_participants_allowed}>"
