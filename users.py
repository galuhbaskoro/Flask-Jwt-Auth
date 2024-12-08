from flask import Blueprint, request, jsonify
from models import User
from schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt # type: ignore

user_bp = Blueprint('users', __name__)

# View Users All
@user_bp.get("/all")
@jwt_required()
def get_all_users():

    claims = get_jwt()

    if claims["is_admin"] == False:
        return jsonify({"message": "You are not authorized"}), 403 
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    
    users = User.query.paginate(page = page, per_page = per_page)
    result = UserSchema().dump(users,many=True)

    return jsonify({"users": result}), 200

# View User by ID
@user_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    result = UserSchema().dump(user)
    return jsonify({"user": result}), 200

# Delete User By ID
@user_bp.delete("/<int:user_id>")
@jwt_required()
def delete_user(user_id):

    claims = get_jwt()

    if claims["is_admin"] == False:
        return jsonify({"message": "You are not authorized"}), 403 

    user = User.query.get_or_404(user_id)
    user.delete()    
    return jsonify({"message": "User deleted"}), 200

# Update User by ID
@user_bp.put("/<int:user_id>")
@jwt_required()    
def update_user(user_id):

    claims = get_jwt()

    if claims["is_admin"] == False:
        return jsonify({"message": "You are not authorized"}), 403

    user = User.query.get_or_404(user_id)    
    data = request.get_json()
    user.username = data.get("username")
    user.email = data.get("email")
    user.role = data.get("role")
    user.update()
    return jsonify({"message": "User updated"}), 200
