from rest_framework import serializers
from .models import Product, ShopCategory, Shop

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields ='__all__'

class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = '__all__'




class ShopSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'phone', 'address', 'logo_url']

    def get_logo_url(self, obj):
        if obj.logo:
            # Assuming you have MEDIA_URL configured in your Django settings
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None
