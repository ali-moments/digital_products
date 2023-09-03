from rest_framework import serializers

from .models import Package, Subscription

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'title', 'sku', 'description', 'avatar', 'price', 'duration')
     
        
class SubscriptionSerializer(serializers.ModelSerializer):
    Package = PackageSerializer()
    
    class Meta:
        model = Subscription
        fields = ('id', 'package', 'created_time', 'expire_time')
        
        