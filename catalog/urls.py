from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('/books/', views.BooksListView.as_view(), name='book-list'),
    # path('/authors/', views.AuthorsListView.as_view(), name='authors-list') ,
    # path('/book/<id:integer>/', views.BookDetailView.as_view(), name='book-detail'),
    # path('/author/<id:integer>/', views.AuthorDetailView.as_view(), name='author-detail'),
] 