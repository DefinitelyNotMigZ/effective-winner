from rest_framework import serializers
from .models import Users, Stores
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["is_staff", "is_active", "is_superuser", "last_login", "date_joined", "groups", "user_permissions"]

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Get the user based on the email
        email = attrs.get('email')
        existing_user = Users.objects.get(email=email)

        # Create refresh and access tokens
        refresh = RefreshToken.for_user(existing_user)

        # Structure the response
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(existing_user.id),
                "email": existing_user.email,
                "first_name": existing_user.first_name,
                "last_name": existing_user.last_name,
                "is_staff": existing_user.is_staff,
            },
        }

        return response_data


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = "__all__"
        read_only_fields = ("user",)


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        attrs['user'] = UserSerializer(user, many=False).data
        attrs.pop("password", None)
        attrs.pop("email", None)
        return attrs
