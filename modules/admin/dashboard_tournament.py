from flask import session
from app import db
from models.tables.tournament import Tournament
from models.tables.event import Event
from models.tables.match import Match
from models.tables.login import Login
from models.tables.permission import Permission
from models.tables.player import Player
from models.tables.result import Result
from models.tables.user_permission import UserPermission
from models.tables.users import Users
from models.tables.players_event_seed import PlayersEventSeed
import json


def post_tournament_details(request):
    db.session.expire_all()
    tournament_name = request.form.get('tournament_name')
    tournament = Tournament.query.filter_by(tournament_name=tournament_name).first()
    events = Event.query.all()
    event_DB = [event.event_name for event in events]
    if tournament:
        if tournament.tournament_name != request.form['tournament_name']:
            tournament.tournament_name = request.form['tournament_name']
        if tournament.location != request.form['location']:
            tournament.location = request.form['location']
        if tournament.registration_open.strftime('%Y-%m-%dT%H:%M') != request.form['registration_open']:
            tournament.registration_open = request.form['registration_open']
        if tournament.registration_closed.strftime('%Y-%m-%dT%H:%M') != request.form['registration_closed']:
            registration_closed = request.form['registration_closed']
        if tournament.tournament_start_date.strftime('%Y-%m-%dT%H:%M') in request.form['tournament_start_date']:
            tournament.tournament_start_date = request.form['tournament_start_date']
        if tournament.tournament_end_date.strftime('%Y-%m-%dT%H:%M') in request.form['tournament_end_date']:
            tournament.tournament_end_date = request.form['tournament_end_date']
        if tournament.announcement != request.form['announcements']:
            tournament.announcement = request.form['announcements']

        events_list_request = json.loads(request.form.getlist('events')[0])
        events_request = [key for event_dict in events_list_request for key in event_dict.keys()]

        events_list = ['MS', 'MD', 'WS', 'WD', 'XD', 'U19', 'U17']
        for event in events_list:
            if event in event_DB and event in events_request:
                event_dict = next((d for d in events_list_request if d.get(event)), None)
                event_entry = Event.query.filter_by(event_name=event).first()
                if event_dict:
                    if event_entry.gender_allowed != event_dict[event]['gender_allowed']:
                        event_entry.gender_allowed = event_dict[event]['gender_allowed']
                    if event_entry.max_participants_allowed != event_dict[event]['max_participants_allowed']:
                        event_entry.max_participants_allowed = event_dict[event]['max_participants_allowed']
                    db.session.commit()
            elif event in event_DB and event not in events_request:
                eventid = Event.query.filter_by(event_name=event).first()
                for event_seed in PlayersEventSeed.query.filter_by(event_id=eventid).all():
                    db.session.delete(event_seed)
                event_entry = Event.query.filter_by(event_name=event).first()
                db.session.delete(event_entry)
                db.session.commit()
            elif event not in event_DB and event in events_request:
                event_dict = next((d for d in events_list_request if d.get(event)), None)
                if event_dict:
                    new_event = Event(event, event_dict[event]['gender_allowed'],
                                      event_dict[event]['max_participants_allowed'])
                    db.session.add(new_event)
                    db.session.commit()
    else:
        tournament_name, location, registration_open, registration_closed, tournament_start_date, tournament_end_date, announcements = '', '', '', '', '', '', ''
        # INSERT to Tournament table
        if 'tournament_name' in request.form:
            tournament_name = request.form['tournament_name']
        if 'location' in request.form:
            location = request.form['location']
        if 'registration_open' in request.form:
            registration_open = request.form['registration_open']
        if 'registration_closed' in request.form:
            registration_closed = request.form['registration_closed']
        if 'tournament_start_date' in request.form:
            tournament_start_date = request.form['tournament_start_date']
        if 'tournament_end_date' in request.form:
            tournament_end_date = request.form['tournament_end_date']
        if 'announcements' in request.form:
            announcements = request.form['announcements']
        # Create a new Tournament object with the details
        new_tournament = Tournament(tournament_name, location, registration_open, registration_closed,
                                    tournament_start_date, tournament_end_date, announcements)
        db.session.add(new_tournament)

        events_list = json.loads(request.form.getlist('events')[0])
        for event_dict in events_list:
            for key in event_dict.keys():
                new_event = Event(key, event_dict[key]['gender_allowed'], event_dict[key]['max_participants_allowed'])
                db.session.add(new_event)

    db.session.commit()

    db.session.expire_all()
    events = Event.query.all()
    event_name = [event.event_name for event in events]
    names_string = ", ".join(event_name)
    # Return the tournament details
    tournament_details = {
        'tournament_name': tournament.tournament_name,
        'location': tournament.location,
        'registration_open': tournament.registration_open,
        'registration_closed': tournament.registration_closed,
        'tournament_start_date': tournament.tournament_start_date,
        'tournament_end_date': tournament.tournament_end_date,
        'event': names_string,
        'announcements': tournament.announcement
    }
    return tournament_details


def get_tournament_details(request):
    # print(Login.query.all())
    tournament_details = {
        'tournament_name': '',
        'location': '',
        'registration_open': '',
        'registration_deadline': '',
        'tournament_start_date': '',
        'tournament_end_date': '',
        'events': [],
        'Regulations': '',
        'announcements': ''
    }
    db.session.expire_all()
    tournament = Tournament.query.all()
    events = Event.query.all()
    if bool(tournament):
        events_list = []
        for event in events:
            events_list.append({
                'name': event.event_name,
                'gender_allowed': event.gender_allowed,
                'max_participants_allowed': event.max_participants_allowed
            })
        tournament_details = {
            'tournament_name': tournament[0].tournament_name,
            'location': tournament[0].location,
            'registration_open': tournament[0].registration_open.strftime('%Y-%m-%dT%H:%M'),
            'registration_closed': tournament[0].registration_closed.strftime('%Y-%m-%dT%H:%M'),
            'tournament_start_date': tournament[0].tournament_start_date.strftime('%Y-%m-%dT%H:%M'),
            'tournament_end_date': tournament[0].tournament_end_date.strftime('%Y-%m-%dT%H:%M'),
            'events': events_list,
            'announcements': tournament[0].announcement
        }
    return tournament_details
