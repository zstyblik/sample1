from django.test import Client
from django.test import TestCase


class TestHealthView(TestCase):

    def test_health(self):
        client = Client()
        response = client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')
