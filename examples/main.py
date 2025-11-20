from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello From Server.507ex!</p>"