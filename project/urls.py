from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import CategoryViewset, AdminCategoryViewset

from shop.views import ProductViewset

from shop.views import ArticleViewset, AdminArticleViewset

#On crée notre router pour toute les classes ici
router=routers.SimpleRouter()
#On déclare enseuile une url basée sur le mot clé "category" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/category'/
router.register('category', CategoryViewset, basename='category')

#On déclare enseuile une url basée sur le mot clé "Product" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/product'/
router.register('product', ProductViewset, basename='product')

#On déclare enseuile une url basée sur le mot clé "Product" et notre
#View afin que l'URL généré soit celle que nous souhaitons 'api/article'/
router.register('article', ArticleViewset, basename='article')

router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/article', AdminArticleViewset, basename='admin-article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

#il faut bien penser à ajouter les urls du router dans la liste des urls
#disponibles
    path('api/', include(router.urls)),

]
