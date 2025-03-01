from flask import Blueprint, request
from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.utils.errors import UnprocessableEntityError, UnauthorizedError
from app.utils.api_responses import build_success_response, build_error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Handle user registration.
    """
    data = request.get_json()

    # Validate input data
    schema = UserRegisterSchema()
    errors = schema.validate(data)

    if errors:
        return build_error_response(message="Invalid input.", status=422, data=errors)

    try:
        user_data = AuthService.register_user(username=data["username"], password=data["password"])
        return build_success_response(message="User registered successfully", data=user_data, status=201)
    
    except UnprocessableEntityError as e:
        return build_error_response(message=str(e), status=422)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Handle user login.
    """
    data = request.get_json()

    schema = UserLoginSchema()
    errors = schema.validate(data)

    if errors:
        return build_error_response(message="Invalid input.", status=422, data=errors)

    try:
        response = AuthService.authenticate_user(username=data["username"], password=data["password"])
        return build_success_response(message="Login successful", data=response)
    
    except UnauthorizedError as e:
        return build_error_response(message=str(e), status=401)