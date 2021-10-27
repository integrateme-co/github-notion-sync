from rest_framework import serializers
from .models import apiStoreModel, integrationModel

class apiStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiStoreModel
        fields = '__all__'

class integrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = integrationModel
        fields = '__all__'