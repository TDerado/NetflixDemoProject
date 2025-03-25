Netflix project:

set up:

git clone https://github.com/TDerado/NetflixDemoProject.git

>cd into folder

pip install -r requirements.txt

>might be needed if database errors:
    flask db init
    flask db migrate -m "message"
    flask db upgrade

python app.py

contains:
    homepage:
        houses all available pages based on if logged in or not
    login:
        log in to a created account
    register:
        creates an user account
    add shows:
        simple form to add shows to the database
    delete show:
        simple form to delete shows from the database
    search:
        displays all shows in the database, allows searching by both title and genre
    favorites:
        shows a users favorited shows
    details:
        displayed all information on a show
        contains the favorite button (a star symbol)
        marks the show as "watched" for the session

