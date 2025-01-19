from rest_framework import serializers
from ...models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        # Überprüfen, ob der Business User ein Anbieter ist
        if 'business_user' in data and data['business_user'].userprofile.type != 'business':
            raise serializers.ValidationError("Reviews can only be given to business users.")

        # Überprüfen, ob die Bewertung zwischen 1 und 5 liegt
        if 'rating' in data and not (1 <= data['rating'] <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        
        return data