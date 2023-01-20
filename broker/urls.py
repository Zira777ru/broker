from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('exchange-rate/', views.exchange_rate, name='exchange_rate'),
    path('trade/', login_required(views.trade), name='trade'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
