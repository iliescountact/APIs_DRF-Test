from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category

class TestCategory (APITestCase) :
#Nous stockons l'url de l'endpoint dans un attribut de classe
#pour pouvoir l'utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')

    def format_datetime(self, value):
        #cette méthode est un helper permettant de formater une date
        #en chaine de caractère sous le même format que celui de l'api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        #cette méthode créer les deux catégories pour celle active et
        #une non-active
        category = Category.objects.create(name='Fruits', active=True)
        # category_empty = Category.objects.create(name='Légumes', active=False)

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
            }
        ]
        self.assertEqual(response.json(), excepted)


    def test_create(self):
        #Nous vérifions qu'aucune catégorie n'existe avant de tenter d'en
        #créer une
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        #Vérifions que le status code est bien en erreur et nous empèche
        #de créer une nouvelle catégorie
        self.assertEqual(response.status_code, 405)
        #Enfin, vérifions qu'aucune nouvelle catégorie n'a été créer malgré
        #le statys code 405
        self.assertFalse(Category.objects.exists())
