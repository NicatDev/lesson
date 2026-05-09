from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        min_length=1,
        help_text=(
            "Ən çox 150 simvol (minimum 1). İcazəli: hərflər, rəqəmlər və @ . + - _ "
            "(Django UsernameValidator qaydaları)."
        ),
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "phone_number")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
