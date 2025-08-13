from rest_framework import serializers

def validate_password_length(password: str):
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    return password