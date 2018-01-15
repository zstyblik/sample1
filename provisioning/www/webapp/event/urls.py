from django.urls import path

from . import views

urlpatterns = [
    path('<int:event_id>/', views.EventView.as_view(), name='event-detail'),
]
