from flask_restful import Resource
from models.post import Post

class Posts(Resource):
    def get(self, name):
        data = Post.find_by_category(name)
        return {
            'filter':'category',
            'category_name': name,
            'data': data
        }
