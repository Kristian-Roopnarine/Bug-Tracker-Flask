from flask import (
    Blueprint, jsonify, request, 
)
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, get_jwt_claims
)
from app.models import db, Users, create_password_hash
import bcrypt

bp = Blueprint('user',__name__,url_prefix='/user')

# route to change password
@bp.route('/password-reset',methods=['PATCH'])
@jwt_required
def change_password():
    # get user information
    user_id = get_jwt_claims()['id']
    # retrieve our user
    user = Users.query.get(user_id)

    # get new password
    new_password = request.json.get('password')
    new_password_confirm = request.json.get('password_confirm')

    if new_password != new_password_confirm:
        return jsonify({'message':'The two passwords do not match'})

    user.password = create_password_hash(new_password)
    db.session.commit()

    return jsonify({'message':'Successfully updated your password! Please relog.'})


"""
# route to send out email
@bp.route('/password-reset-email',methods=['GET','POST'])
@jwt_required
def send_password_reset_email():
    user_id = get_jwt_claims['id']
"""