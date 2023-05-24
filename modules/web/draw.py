from itertools import groupby

from models.models import Users, Event, Match


def get_player_names(player_1_id, player_2_id):
    if player_1_id is None:
        return " "

    player_1 = Users.query.get(player_1_id)
    player_1_name = player_1.first_name + " " + player_1.last_name

    if player_2_id:
        player_2 = Users.query.get(player_2_id)
        player_2_name = player_2.first_name + " " + player_2.last_name
        return player_1_name + " , " + player_2_name
    else:
        return player_1_name


def return_events_with_draws():
    events = {event.event_id: event.event_name for event in Event.query.all() if event.draw_set}
    matches = Match.query.all()
    matches_grouped = groupby(matches, lambda match: match.event_id)

    draws_info = []
    for event_id, matches in matches_grouped:
        draws_set = {'event_id': event_id,
                     'event_name': events[event_id]}
        players = []
        sorted_matches = sorted(matches, key=lambda match: match.draw_no)

        for match in sorted_matches:
            players.append([{'index': match.draw_no,
                             'names': get_player_names(match.side_one_player_1, match.side_one_player_2)},
                            {'index': match.draw_no + 1,
                             'names': get_player_names(match.side_two_player_1, match.side_two_player_2)}])

        draws_set['players'] = players
        draws_info.append(draws_set)

    if not draws_info:
        return False, draws_info
    return True, draws_info
