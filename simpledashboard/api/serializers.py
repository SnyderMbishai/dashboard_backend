from datetime import datetime

from rest_framework import serializers
from .models import Country, Produced, Pending, Rejected
from .helpers import convert_date


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produced
        fields = ("country","units", "date")
        read_only_fields = ["id"]

    def get_fields(self, *args, **kwargs):
        fields = super(ProducerSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "GET":
            fields['date'].required = False
        return fields

class CountrySerializer(serializers.ModelSerializer):
    producer = ProducerSerializer(many=True,read_only=True )
    unit_sum = serializers.IntegerField(read_only=True)
    class Meta:
        model = Country
        fields = ["name", "producer", "unit_sum"]

class RejectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rejected
        fields ="__all__"

class PendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = "__all__"

class RawDataSerializer(serializers.Serializer):
    country = serializers.CharField(required=True, max_length=128)
    date = serializers.CharField(required=True)
    produced = serializers.IntegerField(required=True)
    rejected = serializers.IntegerField(required=True)
    pending = serializers.IntegerField(required=True)

    # def format_date(self, date):
    #     return date.strftime('%d %b %Y %H:%M:%S')

    def validate_produced(self, value):
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationErrror('Not Valid')

    def create(self, validated_data):
        date = convert_date(validated_data["date"])
        validated_data["date"]=date
        country = Country.objects.get_or_create(name=validated_data['country'])
        produced = Produced.objects.create(country=country[0],units=validated_data["produced"], date=validated_data["date"] )
        rejected = Rejected.objects.create(country=country[0],units=validated_data["rejected"], date=validated_data["date"])
        pending = Pending.objects.create(country=country[0],units=validated_data["pending"], date=validated_data["date"])

        obj = {
            "country": CountrySerializer(instance=country[0]).data,
            "produced": ProducerSerializer(instance=produced).data,
            "rejected": RejectedSerializer(instance=rejected).data,
            "pending": PendingSerializer(instance=pending).data
        }
        return obj



