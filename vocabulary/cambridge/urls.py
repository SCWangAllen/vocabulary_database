from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('app',views.app,name='app'),
    path('extension',views.for_extension,name='extension'),
    path('search_result/<str:search_query>/', views.search_result, name='search_result'),

]