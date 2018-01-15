from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.http import JsonResponse
from django.views import View

from events.models import Event


class EventView(View):
    """EventView handles display of one exact event stored in DB."""

    def get(self, request, event_id):
        """Handle GET request and display requested event."""
        try:
            event = Event.objects.get(pk=event_id)
            data = {
                'message': event.message,
                'timestamp': event.timestamp,
                'detail_url': request.build_absolute_uri(),
            }
            status = 200
        except Error:
            data = {
                'error': 'Database connection error'
            }
            status = 500
        except ObjectDoesNotExist:
            data = {
                'error': 'Requested event not found'
            }
            status = 404

        return JsonResponse(data, status=status)
