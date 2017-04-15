# hello.py

#===== MODULES =====#

import sqlite3
from flask import Flask, render_template, g, request, flash
from hashlib import sha256

#===== APP INIT ======#

app = Flask(__name__)

#===== DB CONNECT =====#

DATABASE = "main.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    #returns a TUPLE
    return (rv[0] if rv else None) if one else rv


#===== ROUTES =====#

@app.route("/")
def main():
    # static_url = url_for('static', filename='style.css')
    return render_template("index.html")

@app.route("/data/<int:HomeBound_UID>")
def get_data(HomeBound_UID):
    homeBound = query_db("select * from HomeBound where HomeBoundUID=?",[HomeBound_UID], one=True)
    if homeBound is None:
        return "No such user"
    else:
        return str(homeBound)

@app.route('/logout',)

@app.route('/login', methods=['POST', 'GET'])
def login():
    # error = None
    if request.method == 'POST':

        username = request.form['username']
        passwordChallenge = sha512(request.form['password']).hexdigest()

        user = query_db("select * from Users where UserEmail=?",[username],one=True)
        passwordDB = sha512(user[0]).hexdigest()

        if passwordChallenge == passwordDB:

            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))

        else:
            flask.flash('Incorrect username/password combination.')

        return flask.render_template('login.html', form=form)

#===== DB TEARDOWN =====#

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#===== MAIN RUN ======#

if __name__ == "__main__":
    app.run()
