import json

from django.test import Client, TestCase
from django.urls import reverse

from .models import Event
from .views import (
    _check_mandatory_attrs_present,
    _parse_request_body,
    _validate_timestamp,
    InvalidDataException,
)


def create_event(timestamp, message):
    return Event.objects.create(timestamp=timestamp, message=message)


class EventsViewTest(TestCase):

    def test_get(self):
        events = [
            {
                'message': 'test message1',
                'timestamp': 1515960849,
            },
            {
                'message': 'test message2',
                'timestamp': 1515960850,
            },
        ]
        expected_result = []
        for event in events:
            created_event = create_event(event['timestamp'], event['message'])
            event['event_url'] = 'http://testserver/event/{:d}/'.format(
                created_event.id
            )
            expected_result.append(event)

        client = Client()
        response = client.get('/events')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        pairs = zip(result, expected_result)
        self.assertTrue(any(x != y for x, y in pairs))

    def test_post_event(self):
        event = {
            'timestamp': 12345,
            'message': 'test messsage',
        }
        client = Client()
        response = client.post(
            '/events', data=json.dumps(event), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')

    def test_post_invalid_content_type(self):
        event = {
            'timestamp': 12345,
            'message': 'test messsage',
        }
        expected_content = {
            'error': 'Content-Type application/json is expected'
        }
        client = Client()
        response = client.post(
            '/events', data=event, content_type='text/plain'
        )
        self.assertEqual(response.status_code, 415)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, expected_content)

    def test_post_invalid_data(self):
        test_data = [
            '',
            '{}',
            '{"message": "abc',
        ]
        client = Client()
        for data in test_data:
            response = client.post(
                '/events', data=data, content_type='application/json'
            )
            self.assertTrue(response.status_code in [400, 415])
            content = json.loads(response.content.decode('utf-8'))
            self.assertTrue('error' in content)


class EventsViewSupportFunctionsTests(TestCase):

    def test__check_mandatory_attrs_present(self):
        test_data = [
            {
                'message': 'test message',
                'timestamp': 12345,
            },
            {
                'extra_attr': 'extra attribute',
                'message': 'test message',
                'timestamp': 12345,
            },

        ]
        for data in test_data:
            _check_mandatory_attrs_present(data)

    def test__check_mandatory_attrs_present_raises(self):
        test_data = [
            {
                'message': 'test message',
            },
            {
                'timestamp': 12345,
            },
        ]
        for data in test_data:
            with self.assertRaises(InvalidDataException):
                _check_mandatory_attrs_present(data)

    def test__parse_request_body(self):
        test_data = [
            {
                'body': '{"message": "test message", "timestamp": 12345}',
                'expected': {'message': 'test message', 'timestamp': 12345},
            }
        ]
        for data in test_data:
            parsed_data = _parse_request_body(
                data['body'].encode('utf-8')
            )
            self.assertEqual(parsed_data, data['expected'])

    def test__parse_request_body_invalid(self):
        test_data = [
            'abc',
            '',
            '{}',
            '{"message": "abcd',
        ]
        for data in test_data:
            with self.assertRaises(InvalidDataException):
                _parse_request_body(data.encode('utf-8'))

    def test__validate_timestamp(self):
        test_data = [
            '0',
            '1',
            '123456',
            0,
            1,
            12345,
            1515958659,
        ]
        for data in test_data:
            _validate_timestamp(data)

    def test__validate_timestamp_invalid(self):
        test_data = [
            'abc',
            '0.5',
            '-1000',
            '-1',
            'abc123abc',
            '123abc',
            'abc123',
        ]
        for data in test_data:
            with self.assertRaises(InvalidDataException):
                _validate_timestamp(data)
