from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car
        # plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        category = self.get_object()
        category.active = False
        category.save()

        # Puis désactivons les produits de cette catégorie
        category.products.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()


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

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car
        # plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons les produits
        product = self.get_object()
        product.active = False
        product.save()

        # Puis désactivons les articles de ce produit
        product.articles.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()


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
