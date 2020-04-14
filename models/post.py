from config import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(15), nullable=False,unique=True)
    author = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    encryptionKey = db.Column(db.String(255))

    @classmethod
    def find_by_category(cls, name):
        return cls.query.filter_by(category=name).order_by(Post.date.desc()).all()

    @classmethod
    def find_by_author(cls, name):
        return cls.query.filter_by(author=name).order_by(Post.date.desc()).all()

    @classmethod
    def find_by_serial(cls, serial):
        return cls.query.filter_by(serial=serial).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 