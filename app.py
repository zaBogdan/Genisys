from flask import Flask
from flask_restful import Resource, Api

# Importing the esential falsk tools
from config import db, ma

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://'
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(
        debug=True,
        port=1337
    )