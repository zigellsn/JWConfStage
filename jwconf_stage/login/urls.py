from django.urls import path

from . import views

urlpatterns = [
    path('<str:congregation>', views.index, name='index'),
]
