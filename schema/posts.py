from config import ma
from models.post import Post

class PostsSchema(ma.ModelSchema):
    class Meta:
        model = Post
        load_only = ('encryptionKey',)
        dump_only = ('id','serial','date')