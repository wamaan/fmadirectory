from extensions import db, bcrypt
from flask_login import  UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hash_password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banner_id = db.Column(db.String(255))
    tiger_email = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    personal_email = db.Column(db.String(255))
    current_city = db.Column(db.String(100))
    current_employer = db.Column(db.String(100))
    graduation_date = db.Column(db.String(100))
    linkedin = db.Column(db.String(255))
    graduating_employer = db.Column(db.String(255))
    internship1 = db.Column(db.String(255))
    internship2 = db.Column(db.String(255))
    internship3 = db.Column(db.String(255))
    additional_degrees = db.Column(db.String(255))
    address = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Member {self.first_name}>'
