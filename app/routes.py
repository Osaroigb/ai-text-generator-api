from . import app
from config import logging
from .utils.api_responses import build_error_response, build_success_response
from .utils.errors import UnprocessableEntityError, NotFoundError, OperationForbiddenError


# Define the home route
@app.route("/", methods=['GET', 'POST'])
def home():
    return build_success_response(message='Welcome to AI Text Generator api!')
    

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