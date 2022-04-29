from django.urls import path
from .views import home,userspage,partners,getfilteruser

app_name = "vote"

urlpatterns = [
    path('',home,name="home"),
    path('users/',userspage,name="userspage"),
    path('partners/',partners,name="partners"),
    path('getfilterusers/',getfilteruser,name="getfilteruser")

]