from config import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(10), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(15), nullable=False)
    status = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def find_by_category(cls, name):
        return cls.query.filter_by(category=name).all()

    def find_by_author(cls, name):
        return cls.query.filter_by(author=name).all()

    def find_by_serial(cls, id):
        return cls.query.filter_by(serial=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 