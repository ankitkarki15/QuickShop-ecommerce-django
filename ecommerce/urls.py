from django.contrib import admin
from django.urls import path
from shop import views  # Make sure to import the views from the shop app


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),  # Route for the homepage
    # path('',views.register_page,name="register")
      path('register/', views.register_page, name='register'),
      path('login/', views.login_page, name='login'),
]