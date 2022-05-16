from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import AdminCategoryViewset

from shop.views import ProductViewset

from shop.views import ArticleViewset

#On crée notre router pour la classe Category ici
router_category=routers.SimpleRouter()
#On déclare enseuile une url basée sur le mot clé "category" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/category'/
router_category.register('admin/category', AdminCategoryViewset, basename='admin-category')

#On crée notre router pour la classe Product ici
router_product=routers.SimpleRouter()
#On déclare enseuile une url basée sur le mot clé "Product" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/product'/
router_product.register('product', ProductViewset, basename='product')

#On crée notre router pour la classe Article ici
router_article=routers.SimpleRouter()
#On déclare enseuile une url basée sur le mot clé "Product" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/product'/
router_article.register('article', ArticleViewset, basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

#il faut bien penser à ajouter les urls du router dans la liste des urls
#disponibles
    path('api/', include(router_category.urls)),

    path('api/', include(router_product.urls)),

    path('api/', include(router_article.urls))

]
