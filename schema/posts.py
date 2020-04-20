from config import ma
from models.post import Post
from models.user import User
from schema.users import UserSchema

class PostsSchema(ma.ModelSchema):
    author = ma.Nested(UserSchema)
    class Meta:
        model = Post
        load_only = ('encryptionKey',)
        dump_only = ('id','serial','date','author_id',)
        include_fk = True