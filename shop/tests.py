from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product

class ShopAPITestCase (APITestCase):

    @classmethod
    def setUpTestData (cl):
    #cette méthode créer les deux catégories/product/article
    #pour celle active et non-active
        cl.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cl.product = cl.category.products.create(name='Banane', active=True)
        cl.category.products.create(name='Courgette', active=False)

        cl.category_2 = Category.objects.create(name='Légumes', active=True)
        cl.product_2 = cl.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        #cette méthode est un helper permettant de formater une date
        #en chaine de caractère sous le même format que celui de l'api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")




class TestCategory (ShopAPITestCase) :
#Nous stockons l'url de l'endpoint dans un attribut de classe
#pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')

    def test_list(self):

        #on réalise l'appel en GET en utilisant le client de la classe de
        #tests
        response = self.client.get(self.url)
        #Nous vérifions que le status code est bien 200
        #et qye les valeurs retournes sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'active': category.active,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
                'id': category.id,
                'name': category.name,
            } for category in [self.category, self.category_2]
        ]
        self.assertEqual(response.json(), excepted)


    def test_create(self):
        #Nous vérifions qu'aucune catégorie n'existe avant de tenter d'en
        #créer une
        #self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        #Vérifions que le status code est bien en erreur et nous empèche
        #de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        #Enfin, vérifions qu'aucune nouvelle catégorie n'a été créer malgré
        #le status code 405
        #self.assertFalse(Category.objects.exists())

        category_count = Category.objects.count()
        self.assertEqual(Category.objects.count(), category_count)

#Nouvelle class de test pour la classe Product
class TestProduct (ShopAPITestCase):
#Nous stockons l'url de l'endpoint dans un attribut de classe
#pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('product-list')

    def get_product_detail_data(self, products):
        return [
            {
                'category': product.category,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'id': product.id,
                'name': product.name,
            } for product in products
        ]


    def test_create(self):
        #Nous vérifions qu'aucune catégorie n'existe avant de tenter d'en
        #créer une
        #self.assertFalse(Product.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        #Vérifions que le status code est bien en erreur et nous empèche
        #de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        #Enfin, vérifions qu'aucune nouvelle catégorie n'a été créer malgré
        #le status code 405
        # self.assertFalse(Product.objects.exists())

        product_count = Product.objects.count()
        self.assertEqual(Product.objects.count(), product_count)

    def test_list(self):
        #on réalise l'appel en GET en utilisant le client de la classe de
        #tests
        response = self.client.get(self.url)
        #Nous vérifions que le status code est bien 200
        #et qye les valeurs retournes sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product, self.product_2]), response.json())

    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product]), response.json())

    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
