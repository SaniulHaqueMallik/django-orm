''' 
Serializers transform complex data types into primitive data types (like dictionaries) 
that can be easily converted to JSON or other formats. For example, a serializer can 
convert a Django model instance into a dictionary representation, which can then be 
serialized into JSON for transmission over the network.
'''

from rest_framework import serializers
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
    class Meta: #metadata describing the model
        model = Drink
        fields = ['id', 'name', 'desc']



