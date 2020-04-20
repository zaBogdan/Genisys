import uuid
from flask import request
from flask_restful import Resource
from models.user import User
from schema.users import UserSchema
from config import bcrypt
from flask_jwt_extended import( 
    jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required, fresh_jwt_required
)


schema = UserSchema()
ALLOW_REGISTRATION = True #Change this for security reasons.

class RegisterUser(Resource):
    def post(self):
        if ALLOW_REGISTRATION == False:
            return {"message": "Sorry, but you can't register right now. We have a limited number of users."},401
        data = schema.load(request.get_json())
        if User.find_by_name(data.username):
            return {"message": "This username already exists in our database. Try to login or reset the password"}, 401
        if User.find_by_email(data.email):
            return {"message": "This email already exists in our database. Try to login or reset the password"}, 401
        
        data.uuid = str(uuid.uuid4())
        data.activity = 0
        val = Validation()
        if val.validatePassword(data.password):
                data.password = bcrypt.generate_password_hash(data.password)
        else:
            return {
                "message": "A password must have between 8 and 64 characters long and it must contain letters (uppercase and lowercase) and digits."
            },400
        try:
            data.save_to_db()
            return {"message": "User with uuid `{}` has registered successfully".format(data.uuid)},201
        except:
            return {"message": "There was an error. We can't save this user to our database."},500

class LoginUser(Resource):
    def post(self):
        schema = UserSchema(partial=True)
        data = schema.load(request.get_json())
        user = User.find_by_email(data.email)
        if not user:
            return {"message": "This user doesn't exist in our database."},404
        if not bcrypt.check_password_hash(user.password, data.password):
            return {"message": "Invalid credentials!"},401
        access_token = create_access_token(identity = user.uuid,fresh=True)
        refresh_token = create_refresh_token(identity = user.uuid)
        return {
            "message": "Successfuly logged in!",
            "access_token": access_token,
            "refresh_token": refresh_token
        },200

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def get(self):
        uuid = get_jwt_identity()
        access_token = create_access_token(identity = uuid, fresh=False)
        return {
            "message": "You got a new access token!",
            "access_token": access_token
        },200

class RefreshLogin(Resource):
    @jwt_refresh_token_required
    def post(self):
        schema = UserSchema(partial=True)
        uuid = get_jwt_identity()
        user = User.find_by_uuid(uuid)
        data = schema.load(request.get_json())
        if not data.password:
            return {"message": "You must enter your password!"},401

        if bcrypt.check_password_hash(user.password, data.password):
            access_token = create_access_token(identity = uuid, fresh=True)
            return {
                "message": "Access granted. You have renewed you session",
                "access_token": access_token
            },200
        return {"message": "Wrong password. Try again!"},401

class DumpUsers(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema(many=True)
        users = User.query.order_by(User.activity.desc()).all()
        if not users:
            return {"message":"There are no users registered yet."},404
        return {
            "count": len(users),
            "data": schema.dump(users)
        },200

class EditUser(Resource):
    @fresh_jwt_required
    def put(self, uuid):
        schema = UserSchema(partial=True)
        user = User.find_by_uuid(uuid)
        if not user:
            return {"message": "This user doesn't exist anymore!"},404
        data = schema.load(request.get_json())

        # You can update email and password.
        if not data.email and not data.password:
            return {"message": "There is nothing to change in here."},200
        if data.email:
            if not User.find_by_email(data.email):
                user.email = data.email
            else:
                return {"message": "This email is already linked to another account."},400
        if data.password:
            val = Validation()
            if bcrypt.check_password_hash(user.password,data.password):
                return {"message": "You can't change the password with the old one."},400
            if val.validatePassword(data.password):
                user.password = bcrypt.generate_password_hash(data.password)
            else:
                return {
                "message": "A password must have between 8 and 64 characters long and it must contain letters (uppercase and lowercase) and digits."
                },400
        try:
            user.save_to_db()
            return {"message": "Changes have been updated in our database."},201
        except:
            return {"message": "There was an error on our system and we can't save this to our database. Try again"},500
class DumpUser(Resource):
    @jwt_required
    def get(self, uuid):
        user = User.find_by_uuid(uuid)
        if not user:
            return {"message": "There is no user with the specified UUID."},404
        return {
            "data": schema.dump(user)
        },200

class Validation():
    def validatePassword(self, password):
        import string
        if len(password) < 8 and len(password) > 64:
            return False
        if not any((c in password) for c in string.ascii_letters) or not any((c in password) for c in string.digits):
            return False
        return True
