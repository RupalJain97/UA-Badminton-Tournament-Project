from itertools import groupby
from models.database import db
from models.models import Tournament, Event, Users, Match, PlayersEventSeed


def return_players_name(player_id):
    user_obj = Users.query.get(player_id)
    return " ".join([user_obj.first_name, user_obj.last_name])


def create_match(side_one_player_1, side_one_player_2, side_two_player_1, side_two_player_2, tournament_id, event_id,
                 draw_no):
    # Insert into Match
    db.session.add(
        Match(side_one_player_1=side_one_player_1, side_one_player_2=side_one_player_2,
              side_two_player_1=side_two_player_1, side_two_player_2=side_two_player_2,
              tournament_id=tournament_id, event_id=event_id, match_status="upcoming",
              draw_no=draw_no))

    db.session.commit()
    db.session.expire_all()


def make_draws():
    Match.query.delete()
    db.session.commit()
    db.session.expire_all()

    tournament = Tournament.query.all()  # todo: Get tournament id otherwise
    tournament_id = tournament[0].tournament_id
    """
    Function that is invoked when admin clicks 'make draw' that auto generates draws for everyone.
    """
    db.session.expire_all()
    player_event_seed_table = PlayersEventSeed.query.all()
    event_player_registrations = groupby(player_event_seed_table, lambda entry: entry.event_id)
    draws_info = [make_draw_for_one_event(event, tournament_id) for event in event_player_registrations]
    return draws_info


def make_draw_for_one_event(event, tournament_id):
    # Get event information
    event_id, players = event
    event_details = Event.query.get(event_id)

    # Sort all players by seeding score
    sorted_players = sorted(players, key=lambda player: player.seeding_score)
    number_of_draws: int = int(len(sorted_players) / 2)
    players = []
    index = 1

    for player_no in range(number_of_draws):
        player_set_one = sorted_players[player_no].player_1, sorted_players[player_no].player_2
        player_set_two = sorted_players[-1 - player_no].player_1, sorted_players[-1 - player_no].player_2

        if player_set_one[1] is not None:  # Doubles
            players.append([{'index': index,
                             'names': return_players_name(player_set_one[0]) + " , " + return_players_name(
                                 player_set_one[1])},
                            {'index': index + 1,
                             'names': return_players_name(player_set_one[0]) + " , " + return_players_name(
                                 player_set_one[1])}])
        else:  # Singles
            players.append([{'index': index, 'names': return_players_name(player_set_two[0])},
                            {'index': index + 1, 'names': return_players_name(player_set_two[0])}])

        create_match(player_set_one[0], player_set_one[1], player_set_two[0], player_set_two[1], tournament_id,
                     event_id, index)
        index += 2

    # If there are an odd number of registrations, we pair a player with an empty placeholder player
    if len(sorted_players) % 2 != 0:  # There is an odd number of registrations
        middle_candidate = int(len(sorted_players) / 2)
        player_set = sorted_players[middle_candidate].player_1, sorted_players[middle_candidate].player_2
        if player_set[1] is not None:  # Doubles
            players.append([{'index': index,
                             'names': return_players_name(player_set[0]) + " , " + return_players_name(
                                 player_set[1])},
                            {'index': " ",
                             'names': " "}])
        else:  # Singles
            players.append([{'index': index, 'names': return_players_name(player_set[0])},
                            {'index': " ", 'names': " "}])
        create_match(player_set[0], player_set[1], None, None, tournament_id, event_id, index)

    # Set Event Flag
    event_details.draw_set = True
    db.session.commit()
    db.session.expire_all()

    return {
        'event_id': event_id,
        'event_name': event_details.event_name,
        'players': players
    }
