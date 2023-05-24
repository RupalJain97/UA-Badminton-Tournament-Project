from app import db
from sqlalchemy import ForeignKey
from datetime import datetime

"""
Class Match, stores information relation to match that belongs to a Tournament and an Event
"""


class Match(db.Model):
    __tablename__ = "match"
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.utcnow())
    court_no = db.Column(db.Integer, nullable=True)
    draw_no = db.Column(db.Integer, nullable=True)
    side_one_player_1 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=False)
    side_one_player_2 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=True)
    side_two_player_1 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=True)
    # When odd number of registrations
    side_two_player_2 = db.Column(db.Integer, ForeignKey('player.player_id'), nullable=True)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.tournament_id'), nullable=False)
    event_id = db.Column(db.Integer, ForeignKey('event.event_id'), nullable=False)
    result_id = db.Column(db.Integer, ForeignKey('result.result_id'), nullable=True)
    match_status = db.Column(db.String(30), nullable=False)
    side_one_player_1_rel = db.relationship('Player', foreign_keys=[side_one_player_1],
                                            backref='matches_side_one_player_1')
    side_one_player_2_rel = db.relationship('Player', foreign_keys=[side_one_player_2],
                                            backref='matches_side_one_player_2')
    side_two_player_1_rel = db.relationship('Player', foreign_keys=[side_two_player_1],
                                            backref='matches_side_two_player_1')
    side_two_player_2_rel = db.relationship('Player', foreign_keys=[side_two_player_2],
                                            backref='matches_side_two_player_2')

    def __init__(self, draw_no: int, side_one_player_1: int, side_two_player_1: int, tournament_id: int, event_id: int,
                 match_status: str, result_id: int = None, side_one_player_2: int = None, date: str = None,
                 court_no: int = None,
                 side_two_player_2: int = None) -> None:
        """
        Initialize a Match object with the given attributes.
        date: The date of the match in MM-DD-YYYY format.
        side_one_player_1: The player id of the first player on side one.
        side_one_player_2: The player id of the second player on side one.
        side_two_player_1: The player id of the first player on side two.
        side_two_player_2: The player id of the second player on side two.
        tournament_id: The id of the tournament this match was played in.
        event_id: The id of the event this match was played in.
        result_id: The id of the result of this match.
        match_status: In progress, Upcoming, Finished
        """
        self.date = date
        self.court_no = court_no
        self.draw_no = draw_no
        self.side_one_player_1 = side_one_player_1
        self.side_one_player_2 = side_one_player_2
        self.side_two_player_1 = side_two_player_1
        self.side_two_player_2 = side_two_player_2
        self.tournament_id = tournament_id
        self.event_id = event_id
        self.result_id = result_id
        self.match_status = match_status

    def __repr__(self):
        return f"<Match(match_id={self.match_id},draw_no={self.draw_no} date={self.date}, court_no={self.court_no}," \
               f" side_one_player_1={self.side_one_player_1}," \
               f" side_one_player_2={self.side_one_player_2}, side_two_player_1={self.side_two_player_1}," \
               f" side_two_player_2={self.side_two_player_2}, tournament_id={self.tournament_id}," \
               f" match_status={self.match_status}, event_id={self.event_id}, result_id={self.result_id})>"
