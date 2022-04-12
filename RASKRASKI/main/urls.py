from . import views
from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('create/', create.as_view(), name='create'),
    path('category/<slug:cat_slug>/', show_category.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logoutuser, name='logout'),
]
