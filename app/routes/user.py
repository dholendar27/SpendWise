from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from app.extensions import db, jwt
from app.models import User
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
user = Blueprint('user', __name__)

error_messages = {
    "USER_FOUND" : "User already exists with email",
    "USER_NOT_FOUND" : "User not found",
}

@user.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    elif not data['email']:
        return jsonify({'error': 'No email'}), 400
    elif not data['password']:
        return jsonify({'error': 'No password'}), 400
    elif not data['first_name']:
        return jsonify({'error': 'No first name'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'error': error_messages.get("USER_FOUND")}), 400

    user = User(email=data['email'],firstname=data['first_name'], lastname=data['last_name'] or "")
    user.password = generate_password_hash(data['password'], salt_length=8)
    db.session.add(user)
    db.session.commit()
    return jsonify({'error': 'User created'}), 201


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    user =  User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': error_messages.get("USER_NOT_FOUND")}), 400
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    print(access_token)
    return jsonify({"access_token":access_token,"refresh_token":refresh_token}), 200


@user.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()