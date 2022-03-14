from django.urls import path
from . import views

app_name = 'vote_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('vote/', views.vote_view, name='vote')
]
