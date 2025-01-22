from rest_framework import serializers
from ...models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serialisiert das Review-Modell für die API.
    
    - Enthält Felder für Bewertung, Beschreibung und Benutzerzuordnung.
    - Stellt sicher, dass nur Geschäftsbenutzer bewertet werden können.
    - Validiert, dass die Bewertung zwischen 1 und 5 liegt.
    """
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user',
                            'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Führt benutzerdefinierte Validierungen durch:
        
        - Stellt sicher, dass `business_user` ein Geschäftsbenutzer ist.
        - Überprüft, dass das `rating` zwischen 1 und 5 liegt.
        """
        if 'business_user' in data and data['business_user'].userprofile.type != 'business':
            raise serializers.ValidationError(
                "Reviews can only be given to business users.")

        if 'rating' in data and not (1 <= data['rating'] <= 5):
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")

        return data
