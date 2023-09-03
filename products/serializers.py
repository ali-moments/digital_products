from hashlib import shake_256
from rest_framework import serializers
from .models import Category, Product, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'description', 'avatar')
    
class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'title', 'file_type', 'file')

    def get_file_type(self, file):
        return file.get_file_type_display()
    
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    files = FileSerializer(many=True)
    product_hash = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'categories', 'files', 'url', 'product_hash')
    
    def get_product_hash(self, product):
        return shake_256(f"{product.id} - {product.title}".encode()).hexdigest(10)
