from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from encryption import DataEncryption
from loger import init_log
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# from logging.config import dictConfig


load_dotenv(".env")
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
dataEnc = DataEncryption()
jwt = JWTManager()
log = init_log('api')