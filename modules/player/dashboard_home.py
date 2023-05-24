from flask import session
from sqlalchemy import or_, and_

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


def get_player_details(user_id):
    db.session.expire_all()
    user = Users.query.get(user_id)
    user_details = {'username': user.login_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'player_id': user.id,
                    }

    player = Player.query.get(user_id)
    events_registered = PlayersEventSeed.query.filter(
        or_(PlayersEventSeed.player_1 == player.player_id, PlayersEventSeed.player_2 == player.player_id))
    event_list = []

    events = Event.query.all()
    event_DB = [event.event_name for event in events]

    for event_regis in events_registered:
        # print(event_regis)
        event = Event.query.filter_by(event_id=event_regis.event_id).first()
        event_name = event.event_name
        player2 = None
        # print(event_name, event_regis.player_2)
        if event_regis.player_2 is not None:
            player2 = Users.query.filter_by(id=event_regis.player_2).first()
            player2 = player2.login_id
        event_list.append({event_name: player2})

    # print("List player registeres for: ", event_list)
    player_details = {
        'competing_gender': player.competing_gender,
        'phone_number': player.phone_number,
        'dob': player.dob,
        'club_name': player.club_name,
        'event': event_list,
        'all_events': event_DB
    }

    return {**user_details, **player_details}


def edit_player_details(request, user_id):
    # print("POST: ", request.form)
    msg = ''
    current_user = Users.query.get(user_id)

    if request.form:
        if current_user.email != request.form['email']:
            # Update email in users table

            # Check if email already exists :
            email_exists = Users.query.filter_by(email=request.form['email']).first()
            if email_exists:
                msg += "ERROR : Could not update Email. Email already associated to another account."
            else:
                current_user.email = request.form['email']

    # Update players table
    player_obj = Player.query.get(session['user_id'])

    if request.form['phone_number']: player_obj.phone_number = request.form['phone_number']

    if request.form['dob']: player_obj.dob = request.form['dob']
    if request.form['club_name']: player_obj.club_name = request.form['club_name']

    events = PlayersEventSeed.query.filter(
        or_(PlayersEventSeed.player_1 == player_obj.player_id,
            PlayersEventSeed.player_2 == player_obj.player_id)).all()
    event_reg_in_db = []
    for event in events:
        event_name = Event.query.filter_by(event_id=event.event_id).first()
        event_reg_in_db.append(event_name.event_name)

    # print("DB: ", event_reg_in_db)

    event_registered = json.loads(request.form.get('events'))
    # print("request:", event_registered, list(event_registered.keys()))

    # setAll = set(events_name_list)
    setDB = set(event_reg_in_db)
    setrequest = set(list(event_registered.keys()))
    not_in_request_inDB = setDB.difference(setrequest)
    # not_in_all = setrequest.difference(setAll)
    not_in_db_Inrequest = setrequest.difference(setDB)
    inDB_Inrequest = setrequest.intersection(setDB)

    # print(not_in_request_inDB, not_in_db_Inrequest, inDB_Inrequest)

    for item in not_in_request_inDB:
        # print(item)
        if item not in ['WS', 'MS', 'U19', 'U17']:
            eventid = Event.query.filter_by(event_name=item).first()
            # print(eventid)
            # Delete the events that are present in DB but user deselected the event in dashboard
            # print(PlayersEventSeed.query.filter_by(player_1=player_obj.player_id, event_id=eventid.event_id).all())
            players = PlayersEventSeed.query.filter(
                and_(or_(PlayersEventSeed.player_1 == player_obj.player_id,
                         PlayersEventSeed.player_2 == player_obj.player_id),
                     PlayersEventSeed.event_id == eventid.event_id)
            ).all()
            # print(players)
            for event_seed in players:
                # print(event_seed)
                db.session.delete(event_seed)
                # print(" deleted", event_seed)
        else:
            eventid = Event.query.filter_by(event_name=item).first()
            # print(eventid)
            # Delete the events that are present in DB but user deselected the event in dashboard
            # print(PlayersEventSeed.query.filter_by(player_1=player_obj.player_id, event_id=eventid.event_id).all())
            for event_seed in PlayersEventSeed.query.filter_by(player_1=player_obj.player_id,
                                                               event_id=eventid.event_id).all():
                # print(event_seed)
                db.session.delete(event_seed)
                # print(" deleted", event_seed)

    for item in not_in_db_Inrequest:
        if item not in ['WS', 'MS', 'U19', 'U17']:
            eventid = Event.query.filter_by(event_name=item).first()
            player_2_id = event_registered[item]['partner']
            # print(player_2_id)
            if player_2_id != 'Singles':
                player_2 = Users.query.filter_by(login_id=player_2_id).first()
                # print("player found: ", player_2)
                player_2 = player_2.id
            else:
                player_2 = None
            new_event_seed = PlayersEventSeed(player_1=player_obj.player_id,
                                              player_2=player_2,
                                              seeding_score=0, event_id=eventid.event_id)
            # print(new_event_seed)
            db.session.add(new_event_seed)
        else:
            eventid = Event.query.filter_by(event_name=item).first()
            new_event_seed = PlayersEventSeed(player_1=player_obj.player_id, seeding_score=0, event_id=eventid.event_id)
            db.session.add(new_event_seed)
        db.session.commit()

    for item in inDB_Inrequest:
        # print("present:")
        eventid = Event.query.filter_by(event_name=item).first()
        event_seed = PlayersEventSeed.query.filter_by(player_1=player_obj.player_id, event_id=eventid.event_id).first()
        player_2_id = event_registered[item]['partner']
        # print("player2: ", player_2_id)
        if item not in ['WS', 'MS', 'U19', 'U17']:
            player_2 = Users.query.filter_by(login_id=player_2_id).first()
            if player_2_id == 'Singles':
                player_2 = None
            # print(player_2)
            event_seed.player_2 = player_2.id
        else:
            event_seed.player_2 = None
        # print("Updated: ", event_seed)
        db.session.commit()

    # Loop over the events and update/create the entries in PlayersEventSeed
    # for event_id in event_ids:
    #     print(event_id, event_id[1])
    #     # Check if an entry already exists
    #     event_seed = PlayersEventSeed.query.filter_by(player_1=player_obj.player_id, event_id=event_id[0]).first()
    #
    #     print("Player: ", event_seed)
    #     # If an entry exists, update the fields
    #     if event_seed:
    #         print("present:")
    #         print(event_id[1] in event_registered)
    #         if (event_id[1] in event_registered):
    #             player_2_id = event_registered[event_id[1]]
    #             print(player_2_id['partner'])
    #             if event_id[1] not in ['WS', 'MS', 'U19', 'U17'] and player_2_id != 'Singles':
    #                 player_2 = Users.query.filter_by(login_id=player_2_id['partner']).first()
    #                 print(player_2)
    #                 event_seed.player_2 = player_2.id
    #             else:
    #                 event_seed.player_2 = None
    #
    #             print("Updated: ", event_seed)
    #             db.session.commit()
    #         else:
    #             db.session.delete(event_seed)
    #             db.session.commit()
    #             print(PlayersEventSeed.query.filter_by(player_1=player_obj.player_id, event_id=event_id[0]).first())
    #     # If an entry does not exist, create a new instance of PlayersEventSeed and add it to the database
    #     else:
    #         print("New:")
    #         if request.form.get(event_id[1]) not in ['WS', 'MS', 'U19', 'U17']:
    #             player_2_id = request.form.get(event_id[1] + '_partner', None)
    #             print(player_2_id)
    #             if player_2_id:
    #                 player_2 = Users.query.filter_by(login_id=player_2_id).first()
    #                 print(player_2)
    #                 player_2 = player_2.id
    #             else:
    #                 player_2 = None
    #             new_event_seed = PlayersEventSeed(player_1=player_obj.player_id,
    #                                               player_2=player_2,
    #                                               seeding_score=0, event_id=event_id[0])
    #             db.session.add(new_event_seed)
    #         else:
    #             new_event_seed = PlayersEventSeed(player_1=player_obj.player_id, seeding_score=0, event_id=event_id[0])
    #             db.session.add(new_event_seed)
    #         db.session.commit()

    # Delete the entries that don't have a corresponding event in the event list
    # for event_seed in PlayersEventSeed.query.filter_by(player_1=player_obj.player_id).all():
    #     event = Event.query.get(event_seed.event_id)
    #     if not event or event.event_name not in event_list:
    #         print(" deleted", event_seed)
    #         db.session.delete(event_seed)

    db.session.commit()
    return True, msg
