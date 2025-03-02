from flask import Blueprint, request
from app.services.openai_service import OpenAIService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.generated_text_service import GeneratedTextService
from app.utils.api_responses import build_success_response, build_error_response
from app.schemas.text_schema import GenerateTextSchema, UpdateGeneratedTextSchema
from app.utils.errors import UnprocessableEntityError, NotFoundError, UnauthorizedError

text_bp = Blueprint("text", __name__)


def validate_int(value):
    """Helper function to validate that a value is an integer."""
    try:
        return int(value)
    
    except ValueError:
        raise UnprocessableEntityError("Invalid input: ID of generated text must be an integer.")


@text_bp.route("/", methods=["POST"])
@jwt_required()
def generate_text():
    """
    Generate text using OpenAI and store the response.
    """
    data = request.get_json()

    # Validate request data
    schema = GenerateTextSchema()
    errors = schema.validate(data)

    if errors:
        return build_error_response("Invalid input.", status=422, data=errors)

    try:
        user_id = get_jwt_identity()
        generated_response = OpenAIService.generate_text(prompt=data["prompt"])

        stored_data = GeneratedTextService.store_generated_text(user_id, data["prompt"], generated_response)
        return build_success_response("Text generated successfully.", data=stored_data, status=201)

    except UnprocessableEntityError as e:
        return build_error_response(message=str(e), status=422)
    
    except Exception as e:
        return build_error_response(
            message=str(e),
            status=503
        )


@text_bp.route("/<id>", methods=["GET"])
@jwt_required()
def get_generated_text(id):
    """
    Retrieve a stored generated text by ID.
    """
    try:
        id = validate_int(id)
        user_id = get_jwt_identity()

        generated_text = GeneratedTextService.get_text_by_id(id, int(user_id))
        return build_success_response("Generated text retrieved successfully.", data=generated_text)

    except NotFoundError as e:
        return build_error_response(str(e), status=404)

    except UnauthorizedError as e:
        return build_error_response(str(e), status=403)


@text_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_generated_text(id):
    """
    Update the response of a generated text record.
    """
    data = request.get_json()

    # Validate request data
    schema = UpdateGeneratedTextSchema()
    errors = schema.validate(data)

    if errors:
        return build_error_response("Invalid input.", status=422, data=errors)

    try:
        id = validate_int(id)
        user_id = get_jwt_identity()

        updated_text = GeneratedTextService.update_text(id, int(user_id), data["response"])
        return build_success_response("Generated text updated successfully.", data=updated_text)

    except NotFoundError as e:
        return build_error_response(str(e), status=404)

    except UnauthorizedError as e:
        return build_error_response(str(e), status=403)


@text_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_generated_text(id):
    """
    Delete a stored generated text record.
    """
    try:
        id = validate_int(id)
        user_id = get_jwt_identity()

        GeneratedTextService.delete_text(id, int(user_id))
        return build_success_response("Generated text deleted successfully.")

    except NotFoundError as e:
        return build_error_response(str(e), status=404)

    except UnauthorizedError as e:
        return build_error_response(str(e), status=403)