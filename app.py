from flask import Flask,jsonify
from flask_restful import Api
from os import environ
from marshmallow import ValidationError

# Importing the esential falsk tools
from config import db, ma,bcrypt

# Importing resources
from resources.posts import CategoryPosts,CreatePosts,DumpPosts,AuthorPosts,HandlePosts,ReadEncrypted

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://{}:{}@{}/api'.format(
    environ.get('DB_USER'),
    environ.get('DB_PASSWORD'),
    environ.get('DB_HOSTS')
)

# Create all tables.
@app.before_first_request
def create_tables():
    db.create_all()

# Check for errors in marshmallow
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

#Dumping posts by different stuff
api.add_resource(CategoryPosts, '/posts/category/<string:name>')
api.add_resource(AuthorPosts, '/posts/author/<string:name>')
api.add_resource(DumpPosts, '/posts')

#Creating posts
api.add_resource(CreatePosts, '/post')

#Reading by serial
api.add_resource(HandlePosts, '/post/<string:serial>')
#Reading encrypted data by serial, with the key
api.add_resource(ReadEncrypted, '/post/<string:serial>/<string:key>')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    app.run(
        debug=True,
        port=1337
    )