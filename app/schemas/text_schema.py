from marshmallow import Schema, fields, validate

class GenerateTextSchema(Schema):
    """Schema for validating text generation requests."""
    prompt = fields.Str(
        required=True, 
        validate=validate.Length(min=5, max=1000),
        error_messages={"required": "Prompt is required.", "invalid": "Invalid prompt format."}
    )
    

class UpdateGeneratedTextSchema(Schema):
    """Schema for validating updates to generated text records."""
    response = fields.Str(
        required=True, 
        validate=validate.Length(min=5, max=5000),
        error_messages={"required": "Response is required.", "invalid": "Invalid response format."}
    )