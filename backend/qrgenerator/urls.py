from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_qr, name='generate_qr'),
]
