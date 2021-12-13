from django.urls import path

from . import views

app_name = 'pellet_stove_app'
urlpatterns = [
    path('', views.home, name='home'),
]