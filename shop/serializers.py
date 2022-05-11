from rest_framework.serializers import ModelSerializer

from shop.models import Category
from shop.models import Product
from shop.models import Article

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "date_created", "date_updated", "active"]

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "date_created", "date_updated"]

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "name", "product_id", "active"]
        read_only_fields = ['price']
