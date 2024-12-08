from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_jwt_extended import JWTManager # type: ignore

db = SQLAlchemy()
jwt = JWTManager()