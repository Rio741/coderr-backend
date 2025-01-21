from rest_framework import serializers
from django.db.models import Min
from ...models import Offer, OfferDetail
from user_auth_app.models import UserProfile


class OfferDetailSerializer(serializers.ModelSerializer):
    offer_type = serializers.ChoiceField(choices=OfferDetail.OFFER_TYPES)

    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions",
                  "delivery_time_in_days", "price", "features", "offer_type"]


class OfferListSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description", "created_at", "updated_at",
            "details", "min_price", "min_delivery_time", "user_details"
        ]

    def get_details(self, obj):
        """Gibt nur eine Liste von URLs für OfferDetails zurück."""
        return [{"id": detail.id, "url": f"/offerdetails/{detail.id}/"} for detail in obj.details.all()]

    def get_min_price(self, obj):
        min_price = obj.details.aggregate(min_price=Min("price"))["min_price"]
        return min_price if min_price is not None else 0.0

    def get_min_delivery_time(self, obj):
        min_time = obj.details.aggregate(
            min_time=Min("delivery_time_in_days"))["min_time"]
        return min_time if min_time is not None else 0

    def get_user_details(self, obj):
        try:
            user_profile = obj.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        return {
            "first_name": user_profile.first_name if user_profile and user_profile.first_name else obj.user.first_name,
            "last_name": user_profile.last_name if user_profile and user_profile.last_name else obj.user.last_name,
            "username": obj.user.username,
        }

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def update(self, instance, validated_data):
        """
        Aktualisiert ein `Offer`-Objekt und behandelt `details`, ohne sie doppelt zu speichern.
        """
        details_data = validated_data.pop("details", None)

        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.save()

        if details_data is not None:
            existing_details = {
                detail.id: detail for detail in instance.details.all()}
            request_detail_ids = set()

            for detail_data in details_data:
                detail_id = detail_data.get("id")

                if detail_id and detail_id in existing_details:
                    detail = existing_details[detail_id]
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
                    request_detail_ids.add(detail_id)
                else:
                    new_detail = OfferDetail.objects.create(
                        offer=instance, **detail_data)
                    request_detail_ids.add(new_detail.id)

            details_to_delete = set(
                existing_details.keys()) - request_detail_ids
            OfferDetail.objects.filter(id__in=details_to_delete).delete()

        return instance


class OfferDetailViewSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description", "created_at", "updated_at",
            "details", "min_price", "min_delivery_time", "user_details"
        ]

    def get_min_price(self, obj):
        min_price = obj.details.aggregate(min_price=Min("price"))["min_price"]
        return min_price if min_price is not None else 0.0

    def get_min_delivery_time(self, obj):
        min_time = obj.details.aggregate(
            min_time=Min("delivery_time_in_days"))["min_time"]
        return min_time if min_time is not None else 0

    def get_user_details(self, obj):
        try:
            user_profile = obj.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = None

        return {
            "first_name": user_profile.first_name if user_profile and user_profile.first_name else obj.user.first_name,
            "last_name": user_profile.last_name if user_profile and user_profile.last_name else obj.user.last_name,
            "username": obj.user.username,
        }

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer
