from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('', views.user_login, name='login'),
    path('password_reset/<int:step>', views.password_reset, name='password_reset'),
    path('change_password/<int:user_id>', views.change_password, name='change_password'),
    path('change_password_no_id', views.change_password_no_id, name='change_password_no_id'),
    path('account_locked_page/', views.account_locked_page, name='account_locked_page'),
]