from rest_framework import serializers

from shop.models import Category, Product, Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "name", "active", "price", 'product']

    def validate_price(self,  value):
        #nous vérifions que l'arctile a un prix supérieur à1$
        if value <= 1.0:
        #En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError("Article is less than 1$")
        return value

    def validate_active(self, value):
        #nous vérifions que l'article renseigné est activé
        if value==False:
        #En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError("Article must be activate to create new article")
        return value

    def validate_product(self, value):
    #cette fonction fait le controle de la présence du nom dans la description
        if value.active is False :
        # On fait apparaitre une ValidationError si ce n'est pas le cas
            raise serializers.ValidationError("Inactive product")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "active", 'ecoscore']

class ProductDetailSerializer(serializers.ModelSerializer):
    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans
    # la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits
    # sont multiples pour une catégorie
    articles = ArticleSerializer(many=True)
    class Meta:
        model = Product
        fields = ["id", "name", "active", "articles"]

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'active', 'description']

    def validate_name(self,  value):
        #nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
        #En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError("Category already exists")
        return value

    def validate (self, data):
    #cette fonction fait le controle de la présence du nom dans la description
        if data['name'] not in data['description']:
        # On fait apparaitre une ValidationError si ce n'est pas le cas
            raise serializers.ValidationError("Name Must be in description")
        return data


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
        serializer = ProductListSerializer(queryset, many=True)
        #la propriété '.data' est le rendu de notre serializers
        # que nous retournons ici
        return serializer.data
