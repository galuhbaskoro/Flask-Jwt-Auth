from flask import Blueprint, request, jsonify
from models import Animal
from schemas import AnimalSchema
from flask_jwt_extended import jwt_required, get_jwt # type: ignore

animal_bp = Blueprint('animals', __name__)

# View Animal All
@animal_bp.get("/all")
def get_all_animals():
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    
    animals = Animal.query.paginate(page = page, per_page = per_page)
    result = AnimalSchema().dump(animals,many=True)

    return jsonify({"animals": result}), 200

# View Animal by ID
@animal_bp.get("/<int:animal_id>")
@jwt_required()
def get_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    result = AnimalSchema().dump(animal)
    return jsonify({"animal": result}), 200

# Create Animal
@animal_bp.post("/")
@jwt_required()
def create_animal():

    claims = get_jwt()  

    if claims["is_admin"] == False: 
        return jsonify({"message": "You are not authorized"}), 403

    data = request.get_json()
    new_animal = Animal(
        name = data.get("name"),
        species = data.get("species"),
    )

    new_animal.save()
    return jsonify({"message": "Animal created"}), 201


# Delete User By ID
@animal_bp.delete("/<int:animal_id>")
@jwt_required()
def delete_animal(animal_id):

    claims = get_jwt()

    if claims["is_admin"] == False:
        return jsonify({"message": "You are not authorized"}), 403 

    animal = Animal.query.get_or_404(animal_id)
    animal.delete()    
    return jsonify({"message": "Animal deleted"}), 200

# Update User by ID
@animal_bp.put("/<int:animal_id>")
@jwt_required()    
def update_animal(animal_id):

    claims = get_jwt()

    if claims["is_admin"] == False:
        return jsonify({"message": "You are not authorized"}), 403

    animal = Animal.query.get_or_404(animal_id)    
    data = request.get_json()
    animal.name = data.get("name")
    animal.species = data.get("species")
    animal.update()
    return jsonify({"message": "Animal updated"}), 200
