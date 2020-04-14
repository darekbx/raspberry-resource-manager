from app import db
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def verify_password(self, password):
        password_md5 = hashlib.md5(password.encode())
        return self.password == password_md5.hexdigest()
 
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.name