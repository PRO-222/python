from flask import Flask

app = Flask(__name__)

@app.route("/ver")
def saludar():
    return "<h1> Hola Mundo</h1>"