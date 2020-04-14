from flask import Flask
from flask_restful import Api
from os import environ

# Importing the esential falsk tools
from config import db, ma

# Importing resources
from resources.posts import Posts

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://{}:{}@{}:{}/api'.format(
    environ.get('DB_USER'),
    environ.get('DB_PASSWORD'),
    environ.get('DB_HOST'),
    environ.get('DB_PORT'),
)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Posts, '/posts/category/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(
        debug=True,
        port=1337
    )