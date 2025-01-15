from rest_framework import serializers
from ...models import Order, OfferDetail
from rest_framework.exceptions import ValidationError

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def create(self, validated_data):
        offer_detail_id = self.context['request'].data.get('offer_detail_id')
        
        # Sicherstellen, dass die OfferDetail-ID vorhanden ist
        if not offer_detail_id:
            raise ValidationError({"offer_detail_id": "Dieses Feld ist erforderlich."})

        # Versuche, das OfferDetail zu finden
        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise ValidationError({"offer_detail_id": "Kein OfferDetail mit dieser ID gefunden."})

        # Automatisch Kunden- und Geschäftsnutzer zuweisen
        customer_user = self.context['request'].user

        # Überprüfen, ob der Benutzer ein Kunde ist
        user_profile = getattr(customer_user, 'userprofile', None)
        if not user_profile or user_profile.type != 'customer':
            raise ValidationError({"detail": "Nur Kunden können Bestellungen erstellen."})

        business_user = offer_detail.offer.user

        # Entferne Felder, die explizit übergeben werden
        validated_data.pop('customer_user', None)
        validated_data.pop('business_user', None)

        # Erstelle die Bestellung basierend auf dem Angebotsdetail
        return Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            **validated_data
        )