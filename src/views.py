from impervalib.app import app

@app.route("/")
def list_films():
    return "<p>Hello, World!</p>"

@app.route("/")
def film_info():
    return "<p>Hello, World!</p>"