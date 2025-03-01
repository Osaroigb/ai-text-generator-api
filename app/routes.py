from . import app
from config import logging
from app.controllers.auth_controller import auth_bp
from .utils.api_responses import build_error_response, build_success_response
from .utils.errors import UnprocessableEntityError, NotFoundError, OperationForbiddenError

# Global API prefix
API_PREFIX = "/api"

# Define the home route
@app.route(API_PREFIX, methods=['GET'])
def home():
    return build_success_response(message='Welcome to AI Text Generator api!')
    

# Register authentication routes
app.register_blueprint(auth_bp, url_prefix=API_PREFIX + "/auth")


@app.errorhandler(Exception)
def handle_exception(error):
    # Log the error for debugging purposes
    logging.error(f"Unhandled exception: {error}")
    
    # Check the type of error and customize the response
    if isinstance(error, UnprocessableEntityError):
        response = {"error": error.message, "details": error.verboseMessage}
        http_code = error.httpCode

    elif isinstance(error, NotFoundError):
        response = {"error": error.message, "details": error.verboseMessage}
        http_code = error.httpCode

    elif isinstance(error, OperationForbiddenError):
        response = {"error": error.message, "details": error.verboseMessage}
        http_code = error.httpCode

    else:
        # Default error response if error type is not specifically handled
        response = {"error": "Internal Server Error", "details": "An unexpected error occurred"}
        http_code = 500
    
    return build_error_response(
        message=response["error"],
        status=http_code,
        data=response["details"]
    )