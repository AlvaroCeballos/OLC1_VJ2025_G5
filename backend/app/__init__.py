import os
from flask import Flask
from .routes import routes

class Server:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        template_dir = os.path.join(base_dir, 'frontend', 'templates')
        static_dir = os.path.join(base_dir, 'frontend', 'static')

        self.app = Flask(
            __name__,
            template_folder=template_dir,
            static_folder=static_dir
        )
        self.app.register_blueprint(routes)

    def run(self):
        self.app.run(debug=True)
        