from rest_framework import serializers, fields
from  inventory.models import Inventory

class inventorySerializer(serializers.ModelSerializer):

    batch_date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Inventory 
        fields = '__all__'