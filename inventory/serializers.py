from rest_framework import serializers
from .models import Item  # Import your Item model

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
