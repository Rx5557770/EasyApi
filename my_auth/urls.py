from django.urls import path, include
from my_auth import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.loggout, name='logout'),
    path('change_token/', views.change_token, name='change_token'),
]