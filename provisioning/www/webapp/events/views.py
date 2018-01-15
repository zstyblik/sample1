import json

from django.db import Error
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from .models import Event


class EventsView(View):
    """EventsView displays and stores events."""

    def get(self, request):
        """Handle GET request and return, display, events stored in DB."""
        try:
            data = [
                {
                    'message': event.message,
                    'timestamp': event.timestamp,
                    'event_url': request.build_absolute_uri(
                        reverse('event-detail', args=(event.id,))
                    )
                }
                for event in Event.objects.order_by('-timestamp')
            ]
            status = 200
        except Error:
            data = {
                'error': 'Database connection error'
            }
            status = 500

        return JsonResponse(data, status=status, safe=False)

    def post(self, request):
        """Handle POST request; check contet-type, parse and validate data,
        store event into DB.
        """
        if request.content_type != 'application/json':
            return JsonResponse(
                {'error': 'Content-Type application/json is expected'},
                status=415
            )

        try:
            data = _parse_request_body(request.body)
        except InvalidDataException as exception:
            return JsonResponse({'error': exception.message}, status=400)

        event = Event(
            timestamp=data['timestamp'],
            message=data['message'],
        )
        try:
            event.save()
        except Error:
            return JsonResponse(
                {'error': 'Database connection error'}, status=500
            )

        return JsonResponse({})


class InvalidDataException(Exception):
    """InvalidDataException is raised when data POST-ed by client is found to be
    invalid.
    """

    def __init__(self, message):
        """Constructor.

        :type message: str
        """
        super(InvalidDataException, self).__init__()
        self.message = message


def _check_mandatory_attrs_present(data):
    """Check mandatory attributes are present.

    :type data: dict

    :raises: `InvalidDataException`
    """
    mandatory_attrs = set([
        'message',
        'timestamp',
    ])
    intersection = mandatory_attrs & set(data.keys())
    if intersection != mandatory_attrs:
        raise InvalidDataException(
            'Missing one of mandatory attrs {}'.format(
                ', '.join(mandatory_attrs)
            )
        )


def _parse_request_body(request_body):
    """Parse JSON from HTTP Body and make sure supplied data is valid.

    :type request_body: bytes

    :rtype: dict
    :raises: `InvalidDataException`
    """
    try:
        data = json.loads(request_body.decode('utf-8'))
    except json.JSONDecodeError:
        raise InvalidDataException('Failed to decode JSON')

    _check_mandatory_attrs_present(data)
    _validate_timestamp(data['timestamp'])

    return data


def _validate_timestamp(timestamp):
    """Check given timestamp is valid.

    :type timestamp: int

    :raises: `InvalidDataException`
    """
    try:
        timestamp = int(timestamp)
    except ValueError:
        raise InvalidDataException(
            'Attr timestamp must be of type int'
        )

    if timestamp < 0:
        raise InvalidDataException(
            'Attr timestamp must be greater than 0'
        )
