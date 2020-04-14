from flask import request
from flask_restful import Resource
from models.post import Post
from schema.posts import PostsSchema

schemaMany = PostsSchema(many=True)
schema = PostsSchema()
serial_length = 8 #maximum is 10 for now.

class CategoryPosts(Resource):
    def get(self, name):
        data = Post.find_by_category(name)
        if not data:
            return {"message": "There are no posts yet."},404
        return {
            'category_name': name,
            'count': len(data),
            'data': schemaMany.dump(data)
        }

class AuthorPosts(Resource):
    def get(self, name):
        data = Post.find_by_author(name)
        if not data:
            return {"message": "This author didn't posted yet."},404
        return {
            'author': name,
            'count': len(data),
            'data': schemaMany.dump(data)
        }

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
    def post(self):
        import string, random,datetime
        data = schema.load(request.get_json())
        data.serial = ''.join(random.choices(string.ascii_lowercase + string.digits, k = serial_length)) 
        data.date = datetime.datetime.now()
        #posts with status "ENCRYPTED" must use some encryption.
        if data.encryptionKey:
            return "The AES encryption key is {}".format(data.encryptionKey)
        return "Normal procedure."
        # try:
        #     data.save_to_db()
        #     return {"message": "Post created."},300
        # except:
        #     return {"message":"Something went wrong. We can't upload this in our database."},500

class HandlePosts(Resource):
    def get(self, serial):
        data = Post.find_by_serial(serial)
        if not data:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        return {
            "data": schema.dump(data)
        }

    def put(self, serial):
        schema = PostsSchema(partial=True)
        post = Post.find_by_serial(serial)
        if not post:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        data = schema.load(request.get_json())

        # You can update only title,content and status
        if data.title:
            post.title = data.title
        if data.content:
            post.content = data.content
        if data.status:
            post.status = data.status
        try:
            post.save_to_db()
            return {"message": "Post with serial {} has been updated in our database".format(serial)},300
        except:
            return {"message":"Something went wrong. We can't upload this in our database."},500

    def delete(self, serial):
        post = Post.find_by_serial(serial)
        if not post:
            return {"message": "There is no post with this serial. Please recheck."}, 404
        #Upload this to a new database.
        post.status = 'deleted'
        try:
            post.save_to_db()
            return {"message": "Post with serial {} has been purged from our database".format(serial)},300
        except:
            return {"message":"Something went wrong. We can't upload this in our database."},500

class EncryptAES():
    import base64,hashlib
    # First check to be done here.
    # from Cryptodome.Cipher import AES
    # from Cryptodome import Random
    
    # BLOCK_SIZE = 16
    # pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    # unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    
    # def encrypt(self, raw, password):
    #     private_key = hashlib.sha256(password.encode("utf-8")).digest()
    #     raw = pad(raw)
    #     iv = Random.new().read(AES.block_size)
    #     cipher = AES.new(private_key, AES.MODE_CBC, iv)
    #     return base64.b64encode(iv + cipher.encrypt(raw))
    
    
    # def decrypt(self, enc, password):
    #     private_key = hashlib.sha256(password.encode("utf-8")).digest()
    #     enc = base64.b64decode(enc)
    #     iv = enc[:16]
    #     cipher = AES.new(private_key, AES.MODE_CBC, iv)
    #     return unpad(cipher.decrypt(enc[16:]))