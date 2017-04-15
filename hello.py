# hello.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/profile/<int:shelter_UUID>/<int:homebound_UID>")
def show_profile(shelter_UUID, homebound_UID):
    return render_template("profile.html", shelter_UID=shelter_UID, homebound_UID=homebound_UID)

if __name__ == "__main__":
    app.run()
