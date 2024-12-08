from flask import Flask, jsonify
from extentions import db, jwt
from auth import auth_bp
from users import user_bp
from animals import animal_bp
from models import TokenBlocklist, User

def create_app():
    
    app = Flask(__name__)

    app.config.from_prefixed_env()

    # Initialize Extentions
    db.init_app(app)
    jwt.init_app(app)

    # Blue Print Register
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(animal_bp, url_prefix='/animals')

    # Load User
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.get_user_by_username(username=identity) or None

    # Claims
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = User.get_user_by_username(username=identity)
        if user and user.role == "admin":
            return {"is_admin": True}
        return {"is_admin": False}

    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Request does not contain valid token", "error": "authorization_header"}), 403

    @jwt.token_in_blocklist_loader    
    def check_if_token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data["jti"]    
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    return app