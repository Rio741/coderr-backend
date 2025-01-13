from rest_framework import serializers
from ..models import Offer, OfferDetail
from django.db.models import Min
from rest_framework.reverse import reverse


class OfferDetailSerializer(serializers.ModelSerializer):
    offer_type = serializers.ChoiceField(choices=OfferDetail.OFFER_TYPES)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]

   

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_time=Min('delivery_time_in_days'))['min_time']

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        # Erstelle jedes Detail und ordne es dem Angebot zu
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    

    def update(self, instance, validated_data):
        # Extrahiere die verschachtelten `details`
        details_data = validated_data.pop('details', [])
    
        # Aktualisiere die Hauptfelder des Angebots
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
    
        # Aktualisiere die Details
        existing_details = {detail.id: detail for detail in instance.details.all()}
        request_detail_ids = set()
    
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if not detail_id or detail_id not in existing_details:
                raise serializers.ValidationError(
                    f"Das Detail mit der ID {detail_id} existiert nicht oder ist ungültig."
                )
    
            # Aktualisiere ein existierendes Detail
            detail = existing_details[detail_id]
            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()
    
            request_detail_ids.add(detail_id)
    
        # Prüfe, ob nicht aufgeführte Details entfernt werden sollen (optional)
        # In diesem Fall bleiben alle anderen Details unverändert.
    
        return instance
