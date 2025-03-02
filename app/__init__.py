from flask import Flask
from .config import Config
from flask_cors import CORS
import datetime as datetimeInstance
from flask_jwt_extended import JWTManager

# Initialize the Flask application
app = Flask(__name__)

cors = CORS(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetimeInstance.timedelta(seconds=Config.JWT_EXPIRY_IN_SECONDS)

# Register Flask routes
from . import routes
