from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from models.post import Post
from models.user import User
from schema.posts import PostsSchema
from config import dataEnc,bcrypt, log

schemaMany = PostsSchema(many=True)
schema = PostsSchema()
serial_length = 8 #maximum is 10 for now.

class CategoryPosts(Resource):
    def get(self, name):
        data = Post.find_by_category(name)
        if not data:
            return {"message": "There are no posts in this category yet."},404
        return {
            'count': len(data),
            'data': schemaMany.dump(data)
        },200

class AuthorPosts(Resource):
    def get(self, name):
        user = User.find_by_name(name)
        if not id:
            return {"message": "This author didn't posted yet."},404
        data = Post.find_by_author(user.id)
        if not data:
            return {"message": "This author didn't posted yet."},404
        return {
            'count': len(data),
            'data': schemaMany.dump(data)
        },200

class DumpPosts(Resource):
    def get(self):
        data = Post.query.order_by(Post.date.desc()).all()
        if not data:
            return {"message": "There are no posts yet."},404
        return {
            'count': len(data),
            'data': schemaMany.dump(data)
        },200

class CreatePosts(Resource):
    @jwt_required
    def post(self):
        import string, random,datetime
        data = schema.load(request.get_json())
        data.serial = ''.join(random.choices(string.ascii_lowercase + string.digits, k = serial_length)) 
        data.date = datetime.datetime.now()

        #Handling the author stuff
        from schema.users import UserSchema
        authorData = User.find_by_uuid(get_jwt_identity())
        data.author_id = authorData.id

        #encrypting posts, in the needed cases.
        if data.encryptionKey:
            data.status = 'encrypted'
            try:
                data.content = dataEnc.encodeString(data.content,data.encryptionKey)
                data.encryptionKey = bcrypt.generate_password_hash(data.encryptionKey)
            except Exception as e:
                log.error('Encryption error when creating a post! Check error message: {}'.format(e))
                return {"message": "Internal server error!"},500
        try:
            data.save_to_db() #save the post
            authorData.activity +=1 #increment the activity
            authorData.save_to_db() #save it 
            return {"message": "Post created with serial `{}`.".format(data.serial)},201
        except Exception as e:
            log.error('Database error when creating a new post. Check the error message: {}'.format(e))
            return {"message":"Something went wrong. We can't upload this in our database."},500

class HandlePosts(Resource):
    def get(self, serial):
        data = Post.find_by_serial(serial)
        if not data:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        if data.status == 'encrypted':
            return {"message": 
            "This is an encrypted post. To read it's content you must pass the encryption key"},400
        return {
            "data": schema.dump(data)
        },200
    @jwt_required
    def put(self, serial):
        schema = PostsSchema(partial=True)
        post = Post.find_by_serial(serial)
        if not post:
            return {"message": "There is no post with this serial. Please recheck."}, 404

        #Working only with public data.
        if post.status=='encrypted':
            return {"message": "To make any changes to this post you must pass the encryption key."},400
        
        data = schema.load(request.get_json())
        
        # You can update only title,content and status and category.
        if data.title:
            post.title = data.title
        if data.content:
            post.content = data.content
        if data.category:
            post.category = data.category

        # if you update the status, and pass an encryption key you will encrypt the post. else it will
        # just be changed. 
        if data.status:
            if data.status == 'encrypted':
                if data.encryptionKey:
                    try:
                        post.status = 'encrypted'
                        post.content = dataEnc.encodeString(post.content, data.encryptionKey)
                        post.encryptionKey = bcrypt.generate_password_hash(data.encryptionKey)
                    except Exception as e:
                        log.error("There was an error with encrypting data. Check message: {}".format(e))
                        return {"message": "There was an error with the encryption. Try again."},500
                else:
                    return {
                        "message": "You don't have the encryptionKey. We can't encrypt a message without it."
                    }, 400
            else:
                post.status=data.status
        
        try:
            post.save_to_db()
            return {"message": "Post with serial `{}` has been updated in our database".format(serial)},200
        except Exception as e:
            log.eror("There was an error with updating posts. Check message: {}".format(e))
            return {"message":"Something went wrong. We can't upload this in our database."},500

    @fresh_jwt_required
    def delete(self, serial):
        log.critical("{} tried to delete the post with serial `{}`".format(request.remote_addr, serial))
        return {"message": "Method is still not implemented."}, 500
        post = Post.find_by_serial(serial)
        if not post:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        #Upload this to a new database.
        post.status = 'deleted'
        try:
            post.save_to_db()
            return {"message": "Post with serial `{}` has been purged from our database".format(serial)},202
        except Exception as e:
            log.error("There was a problem when deleting a post. Check message: {}".format(e))
            return {"message":"Something went wrong. We can't upload this in our database."},500

# Create a new method to see encrypted posts. 
class ReadEncrypted(Resource):
    def get(self, serial, key):
        data = Post.find_by_serial(serial)
        if not data:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        if data.status != 'encrypted':
            return {"message": "This post is not encrypted. Everyone can read it."},400

        if bcrypt.check_password_hash(data.encryptionKey, key):
            data.content = dataEnc.decodeString(data.content, key)
        else:
            return {"message": "That's the wrong key. We can't decrypt the message."},401
        
        return {
            "data": schema.dump(data)
        }
    
    @jwt_required
    def put(self, serial,key):
        schema = PostsSchema(partial=True)
        post = Post.find_by_serial(serial)
        if not post:
            return {"message": "There is no post with this serial. Please recheck."},404
        if post.status != 'encrypted':
            return {"message": "This post is not encrypted. Everyone can read it."},400
        if not bcrypt.check_password_hash(post.encryptionKey, key):
            return {"message": "This is the wrong key. We can't decrypt the message, so you can't edit it."}, 401
        
        data = schema.load(request.get_json())
        
        #You can change the title,category, content and status.
        if data.title:
            post.title = data.title
        
        if data.category:
            post.category = data.category
        if data.content:
            post.content = dataEnc.encodeString(data.content, key)

        if data.status and data.status != 'encrypted':
            post.encryptionKey = None #Removing the encryption key.
            post.content = dataEnc.decodeString(post.content, key)
            post.status = data.status
        try:
            post.save_to_db()
            return {"message": "Post with serial `{}` has been updated in our database.".format(serial)},200
        except Exception as e:
            log.error("There was an error when updated an encrypted post. Check message: {}".format(e))
            return {"message":"Something went wrong. We can't upload this in our database."},500
