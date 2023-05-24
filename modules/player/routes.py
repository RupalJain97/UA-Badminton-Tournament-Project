from flask import Blueprint, request, render_template, session, redirect

from modules.decoraters import user_login_required
from modules.player.dashboard_home import edit_player_details, get_player_details

player_app = Blueprint("player", __name__)


@player_app.route('/dashboard', methods=['GET'])
@user_login_required
def player_dashboard():
    player_details = get_player_details(session['user_id'])
    return render_template('player/player_dashboard.html', msg=player_details)


@player_app.route('/edit_details', methods=['POST'])
@user_login_required
def update_player():
    if request.method == "POST":
        update_status, msg = edit_player_details(request, session['user_id'])  # vars for later data validation
        return redirect('/dashboard')
