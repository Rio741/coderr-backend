from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, CustomerProfileSerializer, UserProfileDetailSerializer, BusinessProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from ..models import UserProfile
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound
from django.db import transaction

class RegistrationView(APIView):
    """
    API-View zur Registrierung neuer Benutzer.
    
    - Erstellt einen neuen Benutzer mit den angegebenen Daten.
    - Generiert ein Authentifizierungstoken für den neuen Benutzer.
    - Nutzt eine atomare Transaktion zur Fehlervermeidung.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Registriert einen neuen Benutzer und gibt ein Token zurück."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        "token": token.key,
                        "username": user.username,
                        "email": user.email,
                        "user_id": user.id
                    }, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(
                    {"detail": ["Interner Serverfehler. Bitte versuchen Sie es später erneut."]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    """
    API-View für die Benutzeranmeldung.
    
    - Überprüft die Anmeldedaten.
    - Gibt ein Authentifizierungstoken zurück, wenn die Anmeldung erfolgreich ist.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Authentifiziert einen Benutzer und gibt ein Token zurück."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                }, status=status.HTTP_200_OK)
            return Response({"detail": ["Falsche Anmeldedaten."]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailView(RetrieveUpdateAPIView):
    """
    API-View zur Anzeige und Aktualisierung eines Benutzerprofils.
    
    - Gibt Details eines bestimmten Benutzerprofils basierend auf der ID zurück.
    - Erlaubt das Aktualisieren des Profils für authentifizierte Benutzer.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Holt das Benutzerprofil basierend auf der angegebenen ID."""
        profile_id = self.kwargs.get('pk')

        if isinstance(profile_id, dict):
            profile_id = profile_id.get('pk') or profile_id.get('id')

        if not profile_id:
            raise NotFound("❌ Fehler: Keine gültige ID gefunden.")

        try:
            return UserProfile.objects.get(user__id=profile_id)
        except UserProfile.DoesNotExist:
            raise NotFound("❌ Fehler: Das angeforderte UserProfile existiert nicht.")

class CustomerProfilesListView(ListAPIView):
    """
    API-View zur Auflistung aller Kundenprofile.
    """
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = CustomerProfileSerializer

class BusinessProfilesListView(ListAPIView):
    """
    API-View zur Auflistung aller Geschäftsprofile.
    """
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = BusinessProfileSerializer
