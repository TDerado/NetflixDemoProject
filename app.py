from Netflix import app, db
from Netflix.models import Users, Favorites, Movies_Shows
from flask import render_template
# from flask_restful import Resource

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

# class ShowTitle(Resource):
#     def getByName(self, name):
#         list = Movies_Shows.query.filter(Movies_Shows.title.contains(name))

#         return [show.json for show in list]

# class ShowGenre(Resource):
#     def getByGenre(self, genre):
#         list = Movies_Shows.query.filter_by(genre=genre)

#         return [show.json for show in list]
    
# app.add_resource(ShowTitle, '/serach/<string:name>')
# app.add_resource(ShowGenre, '/serach/<string:genre>')

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)