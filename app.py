from flask import Flask,jsonify
from flask_restful import Api
from os import environ
from marshmallow import ValidationError

# Importing the esential falsk tools
from config import db, ma,bcrypt,jwt,log

# Importing resources
from resources.posts import (
    CategoryPosts,CreatePosts,
    DumpPosts,AuthorPosts,
    HandlePosts,ReadEncrypted
)
from resources.user import (
    RegisterUser, LoginUser,
    RefreshToken, RefreshLogin,
    DumpUsers, EditUser, DumpUser
)

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://{}:{}@{}/api'.format(
    environ.get('DB_USER'),
    environ.get('DB_PASSWORD'),
    environ.get('DB_HOSTS')
)
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

# Create all tables.
@app.before_first_request
def create_tables():
    db.create_all()

# Check for errors in marshmallow
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# ALl endpoints over here

#POSTS 
#Creating posts
api.add_resource(CreatePosts, '/post')
#Dumping posts by different stuff
api.add_resource(CategoryPosts, '/posts/category/<string:name>')
api.add_resource(AuthorPosts, '/posts/author/<string:name>')
api.add_resource(DumpPosts, '/posts/all')
#Reading by serial
api.add_resource(HandlePosts, '/post/<string:serial>')
api.add_resource(ReadEncrypted, '/post/<string:serial>/<string:key>')

#USERS
#Authentification stuff
api.add_resource(RegisterUser, '/users/register')
api.add_resource(LoginUser, '/users/login')
api.add_resource(RefreshToken, '/users/refresh')
api.add_resource(RefreshLogin, '/users/refresh/login')
#Dumping stuff
api.add_resource(DumpUsers, '/users/dump')
api.add_resource(DumpUser, '/users/dump/<string:uuid>')
#Edit users
api.add_resource(EditUser, '/users/edit/<string:uuid>')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.run(
        debug=True,
        port=1337
    )