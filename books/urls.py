from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.book_search_view, name='book_search'),
    path('books/<str:work_id>/', views.book_detail_view, name='book_detail'),
]