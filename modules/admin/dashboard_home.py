from app import db
from models.tables.users import Users


def get_player_roaster():
    db.session.expire_all()
    users = Users.query.all()
    player_roaster = []
    s_no = 1
    for user in users:
        if user.player:
            player_roaster.append({
                'id': s_no,
                'username': user.login_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
            s_no += 1

    return player_roaster
