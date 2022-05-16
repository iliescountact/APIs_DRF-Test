from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response

from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer,CategoryDetailSerializer, ArticleSerializer
from shop.serializers import ProductListSerializer,ProductDetailSerializer

class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    #Ajoutons un attribut de classe qui nous permet de définir notre sérializer
    # de détail
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        #return Category.objects.all()
        return Category.objects.filter(active=True)

    def get_serializer_class(self):
        # Si l'action retourné est un retrieve, alors on retourne le
        # serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer


    def get_queryset(self):
        #on récupére tous les produits dans une variable appelée queryset
        #queryset =  Product.objects.all()
        queryset = Product.objects.filter(active=True)
        #on verifie la présence du paramètre "category_id" dans
        #l'url et si oui alors on applique le filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_serializer_class(self):
        # Si l'action retourné est un retrieve, alors on retourne le
        # serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        # queryset = Article.objects.all()
        #on verifie la présence du paramètre "prduct_id" dans
        #l'url et si oui alors on applique le filtre
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
