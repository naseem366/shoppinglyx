from django.urls import path
from app.api import views

urlpatterns = [
    
    path('api/',views.CustomerListCreate.as_view(),name="api"),
    #path('createapi/',views.CustomerCreate.as_view(),name='createapi')
]