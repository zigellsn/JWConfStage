from django.urls import path

from . import views

app_name = 'receiver'
urlpatterns = [
    path('<str:congregation>/', views.receiver, name='receiver'),
]
