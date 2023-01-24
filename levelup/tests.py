from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient


@override_settings(AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend',))
class LevelUpAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')
        cls.client = APIClient()

    def setUp(self):
        user = User.objects.get(username='test')
        self.client.login(username=user.username, password='test')