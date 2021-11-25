from rest_framework import serializers
from .models import apiStoreModel, integrationModel

class apiStoreSerializer(serializers.ModelSerializer):
    class Meta:
        """Serializer to store API Keys"""
        model = apiStoreModel
        fields = '__all__'

class integrationSerializer(serializers.ModelSerializer):
    class Meta:
        """Serializer for integrations"""
        model = integrationModel
        fields = '__all__'
