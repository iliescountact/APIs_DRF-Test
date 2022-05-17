from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    #On défini les nouveaux API de Token dans un premier temps
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

#il faut bien penser à ajouter les urls du router dans la liste des urls
#disponibles
    path('api/', include(router.urls)),

]
