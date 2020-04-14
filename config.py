from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

db = SQLAlchemy()
ma = Marshmallow()
load_dotenv()