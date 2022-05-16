from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "name", "active"]
        # read_only_fields = ['price']

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "active"]

class ProductDetailSerializer(ModelSerializer):
    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans
    # la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits
    # sont multiples pour une catégorie
    articles = ArticleSerializer(many=True)
    class Meta:
        model = Product
        fields = ["id", "name", "active", "articles"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'active']


class CategoryDetailSerializer(serializers.ModelSerializer):

#On utilise un serializerMethodeField, pour ajouter des
#filtres sur cet appel URL il est nécessaire
#de décrire une méthode nommée 'get_XXX' où XXX est le
#nom de l'attribut, ici 'products'
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'active','products']

    def get_products(self, instance):
        #Le paramètre 'instance' est l'instance de la catégorie
        # consultée.
        # Dans le cas d'une liste, cette méthode est appelée
        # autant de fois qu'il y a d'entité dans la liste

        # On applique le filtre sur notre queryset pour n'avoir
        # que les produits actifs
        queryset = instance.products.filter(active = True)
        #Le serializer est créé avec le queryset défini et
        # toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        #la propriété '.data' est le rendu de notre serializers
        # que nous retournons ici
        return serializer.data
