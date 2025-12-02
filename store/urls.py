from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'), 
    path('category/<slug:category_slug>/', views.book_list, name='book_list_by_category'),
    path('category/<slug:category_slug>/<int:id>/<slug:book_slug>/', views.book_detail, name='book_detail'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
