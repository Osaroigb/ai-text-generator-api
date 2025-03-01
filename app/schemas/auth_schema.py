from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    """Schema for user registration input validation."""
    
    username = fields.Str(
        required=True, 
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "Username is required.", "invalid": "Invalid username format."}
    )
    password = fields.Str(
        required=True, 
        validate=[validate.Length(min=6)],
        error_messages={"required": "Password is required.", "invalid": "Invalid password format."}
    )


class UserLoginSchema(Schema):
    """Schema for user login input validation."""
    
    username = fields.Str(
        required=True, 
        validate=[validate.Length(min=3, max=50)],
        error_messages={"required": "Username is required.", "invalid": "Invalid username format."}
    )
    password = fields.Str(
        required=True, 
        validate=[validate.Length(min=6)],
        error_messages={"required": "Password is required.", "invalid": "Invalid password format."}
    )