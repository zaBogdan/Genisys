from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from encryption import DataEncryption
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

load_dotenv(".env")
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
dataEnc = DataEncryption()
jwt = JWTManager()
