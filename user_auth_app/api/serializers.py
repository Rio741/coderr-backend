from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import UserProfile
from rest_framework import serializers
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
import re


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        errors = {}

        # Prüfe, ob Passwörter übereinstimmen
        if data['password'] != data['repeated_password']:
            errors['password'] = ["Das Passwort ist nicht gleich mit dem wiederholten Passwort."]

        # Prüfe, ob Benutzername bereits existiert
        if User.objects.filter(username=data['username']).exists():
            errors['username'] = ["Dieser Benutzername ist bereits vergeben."]

        # Prüfe, ob E-Mail bereits existiert
        if User.objects.filter(email=data['email']).exists():
            errors['email'] = ["Diese E-Mail-Adresse wird bereits verwendet."]

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')  # Entferne `repeated_password`, da es nicht im User-Modell ist
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(
            user=user,
            type=validated_data['type']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        errors = {}

        if not data.get('username'):
            errors['username'] = ["Benutzername ist erforderlich."]
        if not data.get('password'):
            errors['password'] = ["Passwort ist erforderlich."]

        if errors:
            raise serializers.ValidationError(errors)

        return data


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source="user.id")
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True) 
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            "user", "username", "first_name", "last_name", "email", "file",
            "location", "tel", "description", "working_hours",
            "type", "created_at", "uploaded_at"
        ]

    def get_file(self, obj):
        if obj.file:
            file_url = obj.file.url  

            if file_url.startswith("http"):
                return file_url

            return settings.MEDIA_URL + obj.file.name 

        return None 
    
    def update(self, instance, validated_data):
        request = self.context.get("request")

        # ✅ Überprüfe, ob der angemeldete Benutzer das eigene Profil bearbeitet
        if request.user != instance.user:
            raise PermissionDenied("Sie dürfen nur Ihr eigenes Profil bearbeiten.")  # 403 Forbidden

        # ✅ Falls Datei hochgeladen wird, setze sie
        if "file" in request.FILES:
            instance.file = request.FILES["file"]

        # ✅ Aktualisiere alle anderen Felder
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "last_name"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["user", "file", "uploaded_at", "type"]  

    def get_user(self, obj):
        return {
            "pk": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.first_name if obj.first_name else obj.user.first_name,
            "last_name": obj.last_name if obj.last_name else obj.user.last_name
        }


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    tel = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = [
            "user", "file", "location", "tel", "description",
            "working_hours", "type"
        ]  

    def get_user(self, obj):
        return {
            "pk": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.first_name if obj.first_name else obj.user.first_name,
            "last_name": obj.last_name if obj.last_name else obj.user.last_name
        }
    
    def validate_tel(self, value):
        if not re.match(r"^\+?[0-9]+$", value):
            raise serializers.ValidationError("Die Telefonnummer muss im Format '+49123456789' oder '0123456789' sein.")
        return value