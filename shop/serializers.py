from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class CategorySerializer(ModelSerializer):

    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'active', 'products']

class ArticleSerializer(ModelSerializer):
    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie
    # products_art = ProductSerializer(many=True)
    class Meta:
        model = Article
        fields = ["id", "name", "active", "product"]
        # read_only_fields = ['price']
