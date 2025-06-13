from flask import Flask
from .routes import routes

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(routes)

    def run(self):
        self.app.run(debug = True)
        