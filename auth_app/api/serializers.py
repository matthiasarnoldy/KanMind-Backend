from django.contrib.auth.models import User

from rest_framework import serializers

class RegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value
    
    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("full_name may not be blank")
        return value

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({"error": "passwords don't match"})
        return data

    def create(self, validated_data):
        full_name = validated_data.pop("full_name").strip()
        repeated_password = validated_data.pop("repeated_password")
        email = validated_data["email"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=full_name,
        )
        return user