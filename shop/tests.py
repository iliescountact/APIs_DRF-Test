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

        cl.product = cl.category.products.create(name='Ananas', active=True)
        cl.category.products.create(name='Banane', active=False)

        cl.category_2 = Category.objects.create(name='Légumes', active=True)
        cl.product_2 = cl.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        #cette méthode est un helper permettant de formater une date
        #en chaine de caractère sous le même format que celui de l'api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_article_list_data(self, articles):
        return [
            {
                'id': article.id,
                'name': article.name,
                # 'date_created': self.format_datetime(article.date_created),
                # 'date_updated': self.format_datetime(article.date_updated),
                'product': article.product_id
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.id,
                'name': product.name,
                'active': product.active,
                #'category': product.category_id,
                # 'articles':self.get_article_list_data(product.articles.filter(active=True)),
            } for product in products
        ]

    def get_category_list_data(self, categories):
        return [
            {
                'id': category.id,
                # 'date_created': self.format_datetime(category.date_created),
                # 'date_updated': self.format_datetime(category.date_updated),
                'name': category.name,
                'active': category.active,
                # 'products':self.get_product_list_data(category.products.filter(active=True)),
            } for category in categories
        ]

class TestCategory (ShopAPITestCase) :
#Nous stockons l'url de l'endpoint dans un attribut de classe
#pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')

    # def test_detail(self):
    #     # Nous utilisons l'url de détail
    #     url_detail = reverse('category-detail',kwargs={'pk': self.category.pk})
    #     response = self.client.get(url_detail)
    #     # Nous vérifions également le status code de retour ainsi que les données reçues
    #     self.assertEqual(response.status_code, 200)
    #     excepted = {
    #         'id': self.category.pk,
    #         'name': self.category.name,
    #         'products': self.get_product_list_data(self.category.products.filter(active=True)),
    #     }
    #     self.assertEqual(excepted, response.json())

    def test_list(self):
        #on réalise l'appel en GET en utilisant le client de la classe de
        #tests
        response = self.client.get(self.url)
        #Nous vérifions que le status code est bien 200
        #et qye les valeurs retournes sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        #Nous vérifions que la réponse renvoyé correspond bien
        #aux données que nous affichons côté front
        self.assertEqual(response.json()['results'], self.get_category_list_data([self.category, self.category_2]))


    def test_create(self):
        #Nous vérifions qu'aucune catégorie n'existe avant de tenter d'en
        #créer une
        category_count = Category.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        #Vérifions que le status code est bien en erreur et nous empèche
        #de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        #Enfin, vérifions qu'aucune nouvelle catégorie n'a été créer malgré
        #le status code 405
        self.assertEqual(Category.objects.count(), category_count)

#Nouvelle class de test pour la classe Product
class TestProduct (ShopAPITestCase):
#Nous stockons l'url de l'endpoint dans un attribut de classe
#pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('product-list')

    def test_list(self):
        #on réalise l'appel en GET en utilisant le client de la classe de
        #tests
        response = self.client.get(self.url)
        #Nous vérifions que le status code est bien 200
        #et qye les valeurs retournes sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        #Nous vérifions que la réponse renvoyé correspond bien
        #aux données que nous affichons côté front
        self.assertEqual(response.json()['results'], self.get_product_list_data([self.product, self.product_2]))


    def test_create(self):
        #Nous vérifions qu'aucune catégorie n'existe avant de tenter d'en
        #créer une
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        #Vérifions que le status code est bien en erreur et nous empèche
        #de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        #Enfin, vérifions qu'aucune nouvelle catégorie n'a été créer malgré
        #le status code 405
        self.assertEqual(Product.objects.count(), product_count)

    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product]), response.json()['results'])

    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
