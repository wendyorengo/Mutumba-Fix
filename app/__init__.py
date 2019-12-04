from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config_options

bootstrap = Bootstrap(app)
mail = Mail
def create_app(config_name):

    app = Flask(__name__)
    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)

    return app







