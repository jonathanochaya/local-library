from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('authors/', views.AuthorsListView.as_view(), name='authors-list') ,
    # path('book/<int:id>/', views.BookDetailView.as_view(), name='book-detail'),
    # path('author/<int:id>/', views.AuthorDetailView.as_view(), name='author-detail'),
] 