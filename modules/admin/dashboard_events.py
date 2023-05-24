from app import db
from models.tables.users import Users
from models.tables.players_event_seed import PlayersEventSeed
from models.tables.event import Event


def assign_seeding(request, event_details):
    ms_events_details = event_details["ms_events_details"]
    ws_events_details = event_details["ws_events_details"]
    md_events_details = event_details["md_events_details"]
    wd_events_details = event_details["wd_events_details"]
    xd_events_details = event_details["xd_events_details"]
    u19_events_details = event_details["u19_events_details"]
    u17_events_details = event_details["u17_events_details"]

    data = request.form
    seed_list = data.getlist('seed')
    if 'ms_events_details' in data:
        i = 0
        for entry in ms_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'ws_events_details' in data:
        i = 0
        for entry in ws_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'md_events_details' in data:
        i = 0
        for entry in md_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'wd_events_details' in data:
        i = 0
        for entry in wd_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'xd_events_details' in data:
        i = 0
        for entry in xd_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'u17_events_details' in data:
        i = 0
        for entry in u17_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1
    elif 'u19_events_details' in data:
        i = 0
        for entry in u19_events_details:
            entry['seed'] = seed_list[i]
            seed_table_entry = PlayersEventSeed.query.filter_by(players_event_seed_id=entry['event_table_id']).first()
            seed_table_entry.seeding_score = entry['seed']
            db.session.commit()
            i += 1

    return {"ms_events_details": ms_events_details,
            "ws_events_details": ws_events_details,
            "md_events_details": md_events_details,
            "wd_events_details": wd_events_details,
            "xd_events_details": xd_events_details,
            "u19_events_details": u19_events_details,
            "u17_events_details": u17_events_details
            }


def get_event_details():
    db.session.expire_all()
    all_registrations = PlayersEventSeed.query.all()
    all_events = Event.query.all()
    ms_events_details = []
    ws_events_details = []
    md_events_details = []
    wd_events_details = []
    xd_events_details = []
    u19_events_details = []
    u17_events_details = []

    for event in all_events:
        if event.event_name == 'MS':
            ms_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    ms_events_details.append({
                        'id': ms_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    ms_no += 1
        elif event.event_name == 'WS':
            ws_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    ws_events_details.append({
                        'id': ws_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    ws_no += 1
        elif event.event_name == 'MD':
            md_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    user2_entry = Users.query.filter_by(id=reg_entry.player_2).first()
                    md_events_details.append({
                        'id': md_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'player2': user2_entry.first_name + ' ' + user2_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    md_no += 1
        elif event.event_name == 'WD':
            wd_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    user2_entry = Users.query.filter_by(id=reg_entry.player_2).first()
                    wd_events_details.append({
                        'id': wd_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'player2': user2_entry.first_name + ' ' + user2_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    wd_no += 1
        elif event.event_name == 'XD':
            xd_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    user2_entry = Users.query.filter_by(id=reg_entry.player_2).first()
                    xd_events_details.append({
                        'id': xd_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'player2': user2_entry.first_name + ' ' + user2_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    xd_no += 1
        elif event.event_name == 'U19':
            u19_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    u19_events_details.append({
                        'id': u19_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    u19_no += 1
        elif event.event_name == 'U17':
            u17_no = 1
            for reg_entry in all_registrations:
                if reg_entry.event_id == event.event_id:
                    user1_entry = Users.query.filter_by(id=reg_entry.player_1).first()
                    u17_events_details.append({
                        'id': u17_no,
                        'player1': user1_entry.first_name + ' ' + user1_entry.last_name,
                        'seed': reg_entry.seeding_score,
                        'event_table_id': reg_entry.players_event_seed_id
                    })
                    u17_no += 1

    return {"ms_events_details": ms_events_details,
            "ws_events_details": ws_events_details,
            "md_events_details": md_events_details,
            "wd_events_details": wd_events_details,
            "xd_events_details": xd_events_details,
            "u19_events_details": u19_events_details,
            "u17_events_details": u17_events_details
            }
