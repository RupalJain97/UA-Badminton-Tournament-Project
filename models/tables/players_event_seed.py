from app import db
from sqlalchemy import ForeignKey

"""
This table stores the (player that plays individually) or (players that form a team) for an EVENT.
This table will also store the seeding value that the admin will update. 
It's a many-to-many relationship between event & players.
An event can be played by many players, A player can play many events.
"""


class PlayersEventSeed(db.Model):
    __tablename__ = "players_event_seed"
    players_event_seed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_1 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=False)
    player_2 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=True)
    seeding_score = db.Column(db.Integer, default=0)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    player_1_rel = db.relationship('Player', foreign_keys=[player_1], backref='seed_player_1')
    player_2_rel = db.relationship('Player', foreign_keys=[player_2], backref='seed_player_2')

    def __init__(self, player_1: int, seeding_score: int, event_id: int, player_2: int = None) -> None:
        """
        Initialize a PlayersEventSeed object with the given attributes.
        player_1: The ID of the first player.
        seeding_score: The seeding score for the team or individual.
        event_id: The ID of the event the seed is for.
        player_2: The ID of the second player (optional, for doubles events).
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self.seeding_score = seeding_score
        self.event_id = event_id

    def __repr__(self) -> str:
        """Return a string representation of the players_event_seed object."""
        return f"<PlayersEventSeed(players_event_seed_id={self.players_event_seed_id}, player_1={self.player_1}, " \
               f"player_2={self.player_2}, seeding_score={self.seeding_score}, event_id={self.event_id})>"
