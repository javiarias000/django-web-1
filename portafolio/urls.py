from django.urls import path
from .views import base_view, set_language

urlpatterns = [
    path('', base_view, name='base'),
    path('language/<str:language>/', set_language, name='set_language'),
]
