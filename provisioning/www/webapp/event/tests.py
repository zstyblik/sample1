import json

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from events.models import Event


def create_event(timestamp, message):
    return Event.objects.create(timestamp=timestamp, message=message)


class EventViewTest(TestCase):

    def test_get_event(self):
        timestamp = 1515960849
        message = 'test message'
        event = create_event(timestamp, message)
        url = reverse('event-detail', args=(event.id,))
        expected_content = {
            'detail_url': 'http://testserver/event/{:d}/'.format(event.id),
            'message': message,
            'timestamp': timestamp,
        }
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, expected_content)

    def test_get_even_nonexistent(self):
        expected_content = {'error': 'Requested event not found'}
        url = reverse('event-detail', args=(9999,))
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, expected_content)
