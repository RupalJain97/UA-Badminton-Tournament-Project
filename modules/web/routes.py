from flask import Blueprint, render_template, request

from modules.admin.dashboard_home import get_player_roaster
from modules.admin.dashboard_events import get_event_details
from modules.admin.dashboard_matches import get_public_matches_details
from modules.web.draw import return_events_with_draws
from modules.admin.dashboard_tournament import get_tournament_details

web_app = Blueprint("web", __name__)


@web_app.route('/', methods=['GET', 'POST'])
def home():
    tournament_overview = get_tournament_details(request)
    return render_template('web/home.html', msg = tournament_overview)


@web_app.route('/tournament')
def tournament():
    tournament_details = get_tournament_details(request)
    return render_template('web/tournament.html', msg = tournament_details)


@web_app.route('/players')
def public_view_players():
    player_details = get_player_roaster()
    return render_template('web/players.html', msg=player_details)


@web_app.route('/events')
def events():
    event_details = get_event_details()
    return render_template('web/events.html', msg=event_details)


@web_app.route('/draws')
def draws():
    draws_boolean, draws_info = return_events_with_draws()
    if draws_boolean:
        return render_template('web/draws.html', msg=draws_info)
    else:
        return render_template('web/draws.html')


@web_app.route('/matches')
def matches():
    match_details = get_public_matches_details()
    return render_template('web/matches.html', msg=match_details)
