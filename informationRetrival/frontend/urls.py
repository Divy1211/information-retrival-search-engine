from django.conf.urls import url
from . import views

app_name = 'frontend'
urlpatterns = [
    url('^$', views.index, name='index'),
]