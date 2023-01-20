from django.urls import path

from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('company/<slug:company_slug>/', views.company_page, name='company_page'),
    path('add-company/', views.add_company, name='add_company'),

]