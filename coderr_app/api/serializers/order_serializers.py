from rest_framework import serializers
from ...models import Order, OfferDetail
from rest_framework.exceptions import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_user', 'business_user',
                            'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def create(self, validated_data):
        offer_detail_id = self.context['request'].data.get('offer_detail_id')

        if not offer_detail_id:
            raise ValidationError(
                {"offer_detail_id": "Dieses Feld ist erforderlich."})

        try:
            offer_detail = OfferDetail.objects.select_related(
                'offer').get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise ValidationError(
                {"offer_detail_id": "Kein OfferDetail mit dieser ID gefunden."})

        customer_user = self.context['request'].user

        user_profile = getattr(customer_user, 'userprofile', None)
        if not user_profile or user_profile.type != 'customer':
            raise ValidationError(
                {"detail": "Nur Kunden können Bestellungen erstellen."})

        business_user = offer_detail.offer.user
        print(f"✅ OfferDetail ID: {offer_detail_id}")
        print(f"🔍 Offer User ID: {business_user.id if business_user else 'None'}")

        if not business_user:
            raise ValidationError(
                {"business_user": "Kein Business-User gefunden!"})

        validated_data.pop('customer_user', None)
        validated_data.pop('business_user', None)

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
