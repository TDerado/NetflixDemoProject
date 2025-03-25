from flask import render_template, url_for, flash, redirect, Blueprint, session
from flask_login import current_user
from Netflix import db
from Netflix.models import Movies_Shows, Favorites
from Netflix.shows.forms import AddShow, DeleteShow, SearchShows

shows = Blueprint('shows', __name__)

@shows.route('/add', methods=['GET', 'POST'])
def add():
    if '_flashes' in session:
        session['_flashes'].clear()

    form = AddShow()
    form2 = DeleteShow()

    if form.validate_on_submit():
        show = Movies_Shows(title=form.title.data, genre=form.genre.data, description=form.description.data,
                            release_date=form.release_date.data, duration=form.duration.data)

        db.session.add(show)
        db.session.commit()
        flash("Added")
        return render_template('add_shows.html', form=form)
    return render_template('add_shows.html', form=form)

@shows.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteShow()   
    if form.validate_on_submit():
        show = Movies_Shows.query.filter_by(title=form.title.data).first()

        if show is not None:
            db.session.delete(show)
            db.session.commit()
            flash("Deleted")
        return render_template('delete_show.html', form=form)
    return render_template('delete_show.html', form=form)

@shows.route('/search', methods=['GET', 'POST'])
def search():
    if '_flashes' in session:
        session['_flashes'].clear()
    form = SearchShows()
    if form.validate_on_submit():
        if form.title.data is not None and form.title.data != "":
            if form.genre.data is not None and form.genre.data != "":
                list = Movies_Shows.query.filter(Movies_Shows.title.contains(form.title.data), Movies_Shows.genre.contains(form.genre.data)).order_by(Movies_Shows.title).all()
            else:
                list = Movies_Shows.query.filter(Movies_Shows.title.contains(form.title.data)).order_by(Movies_Shows.title).all()
        else:
            if form.genre.data is not None and form.genre.data != "":
                list = Movies_Shows.query.filter(Movies_Shows.genre.contains(form.genre.data)).order_by(Movies_Shows.title).all()
            else:
                list = Movies_Shows.query.order_by(Movies_Shows.title).all()

        return render_template('search.html', form=form, shows=list, watched=session["watched"])
    list = Movies_Shows.query.order_by(Movies_Shows.title).all()
    return render_template('search.html', form=form, shows=list, watched=session["watched"])

@shows.route('/details/<id>', methods=['GET', 'POST'])
def details(id):

    user_id = current_user.id

    favorited = Favorites.query.filter(Favorites.user_id==user_id, Favorites.Show_id==id).first()
    ifFavorited = False
    if favorited is not None:
        ifFavorited = True

    tmp = session["watched"]
    tmp.append(id)
    session["watched"] = tmp

    show = Movies_Shows.query.filter_by(id=id).first()
    return render_template('details.html', show=show, favorited=ifFavorited)