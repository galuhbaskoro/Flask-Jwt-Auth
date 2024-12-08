from flask import Blueprint, jsonify, request
from models import TokenBlocklist, User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required # type: ignore

auth_bp = Blueprint('auth', __name__)

# Register
@auth_bp.post('/register')
def register_user():
    
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409
    
    new_user = User(
        username = data.get("username"),
        email = data.get("email"),
        role = data.get("role"),
    )
    
    new_user.set_password(
        password = data.get("password")
    )

    new_user.save()
    
    return jsonify({"message": "User created"}), 201

# Login
@auth_bp.post('/login')
def login_user():

    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))

    if user and (user.check_password(password= data.get("password"))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify(
            {
                "message" : "Successfully Logged in",
                "tokens" : {
                    "access" : access_token,
                    "refresh" : refresh_token
                } 
            }
        ), 200
    
    return jsonify({"error" : "Invalid username or password"}), 400

# Logout
@auth_bp.get('/logout')
@jwt_required()
def logout_user():
    jti = get_jwt()["jti"]
    token_blocklist = TokenBlocklist(jti=jti)
    token_blocklist.save()
    return jsonify({"message" : "Successfully logged out"}), 200  

# Who Am I
@auth_bp.get('/me')
@jwt_required()
def who_am_i():
    claims = get_jwt()
    return jsonify({"claims" : claims}), 200
