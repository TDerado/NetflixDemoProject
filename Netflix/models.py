from Netflix import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_login import current_user, login_required

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movies_Shows(db.Model):

    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    genre = db.Column(db.String(64))
    description = db.Column(db.String(250))
    release_date = db.Column(db.String(16))
    duration = db.Column(db.Integer)
    favorites = db.relationship('Favorites', backref='author', lazy=True)

    def __init__(self, title, genre, description, release_date, duration):
        self.title = title
        self.genre = genre
        self.description = description
        self.release_date = release_date
        self.duration = duration

class Favorites(db.Model):

    users = db.relationship(Users)
    shows = db.relationship(Movies_Shows)

    __tablename__ = 'Favorites'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)

    def __init__(self, user_id, show_id):
        self.user_id = user_id
        self.Show_id = show_id

    def favorited(show_id):
        find = Favorites.query.filter(Favorites.user_id==current_user.id, Favorites.Show_id==show_id).first()
        if find is None:
            return False
        return True
