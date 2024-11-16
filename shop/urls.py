from django.urls import path
from . import views

# urls for view page
urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register_page, name='register'),  
    path('login/', views.login_page, name='login'),  
]