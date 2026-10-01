from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "preferences",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "Name must contain at least 2 characters."
            )

        return value

    def validate_email(self, value):
        return value.strip().lower()

    def validate_preferences(self, value):

        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Preferences must be an object."
            )

        allowed_keys = {
            "genres",
            "artists",
            "moods",
        }

        invalid_keys = set(value.keys()) - allowed_keys

        if invalid_keys:
            raise serializers.ValidationError(
                f"Unsupported preference fields: "
                f"{', '.join(sorted(invalid_keys))}"
            )

        for key in allowed_keys:
            if key in value:

                if not isinstance(value[key], list):
                    raise serializers.ValidationError(
                        f"'{key}' must be a list."
                    )

                for item in value[key]:

                    if not isinstance(item, str):
                        raise serializers.ValidationError(
                            f"All values inside '{key}' must be strings."
                        )

                    if not item.strip():
                        raise serializers.ValidationError(
                            f"'{key}' cannot contain empty values."
                        )

        return value