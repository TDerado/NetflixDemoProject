from flask import render_template, url_for, flash, redirect, Blueprint
from Netflix import db
from Netflix.models import Movies_Shows
from Netflix.shows.forms import AddShow, DeleteShow, SearchShows

shows = Blueprint('shows', __name__)

@shows.route('/add', methods=['GET', 'POST'])
def add():
    form = AddShow()
    form2 = DeleteShow()

    if form.validate_on_submit():
        show = Movies_Shows(title=form.title.data, genre=form.genre.data, description=form.description.data,
                            release_date=form.release_date.data, duration=form.duration.data)

        db.session.add(show)
        db.session.commit()
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
            return redirect(url_for('shows.add'))
        return render_template('delete_show.html', form=form)
    return render_template('delete_show.html', form=form)

@shows.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchShows()
    if form.validate_on_submit():
        if form.title.data is not None and form.title.data != "":
            if form.genre.data is not None and form.genre.data != "":
                list = Movies_Shows.query.filter(Movies_Shows.title.contains(form.title.data), Movies_Shows.genre==form.genre.data).order_by(Movies_Shows.title).all()
            else:
                list = Movies_Shows.query.filter(Movies_Shows.title.contains(form.title.data)).order_by(Movies_Shows.title).all()
        else:
            if form.genre.data is not None and form.genre.data != "":
                list = Movies_Shows.query.filter_by(genre=form.genre.data).order_by(Movies_Shows.title).all()
            else:
                list = Movies_Shows.query.order_by(Movies_Shows.title).all()

        return render_template('search.html', form=form, shows=list)
    return render_template('search.html', form=form, shows=[])

@shows.route('/details/<id>', methods=['GET', 'POST'])
def details(id):
    show = Movies_Shows.query.filter_by(id=id).first()
    return render_template('details.html', show=show)