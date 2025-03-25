from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Netflix import db
from werkzeug.security import generate_password_hash,check_password_hash
from Netflix.models import Users, Favorites, Movies_Shows
from Netflix.users.forms import RegisterForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = Users(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')

            return render_template('home.html')

    return render_template('login.html', form=form)

@users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/favoriteShow/<show_id>', methods=['GET', 'POST'])
def favoriteShow(show_id):

    if Favorites.favorited(show_id=show_id):
        favorite = Favorites.query.filter(Favorites.user_id==current_user.id, Favorites.Show_id==show_id).first()
        db.session.delete(favorite)
        db.session.commit()
    else:
        favorite = Favorites(user_id=current_user.id, show_id=show_id)
        db.session.add(favorite)
        db.session.commit()

    return redirect(url_for('users.favorites'))

@users.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    user_id = current_user.id

    favorites_list = Favorites.query.filter_by(user_id=user_id).all()

    showList = []
    for fav in favorites_list:
        showList.append(Movies_Shows.query.get(fav.Show_id))

    return render_template('favorites.html', favorites=showList)