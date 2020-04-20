from config import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), nullable=False,unique=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False,unique=True)
    activity = db.Column(db.Integer(), default=0)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_email(cls, mail):
        return cls.query.filter_by(email=mail).first()
    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 