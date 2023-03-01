from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    models = Book

    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

    # override default model queryset with custom one
    def get_queryset(self):
        return Book.objects.all()[:5]
    
    # supply additional context variables to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_variable'] = 'This is to test the get_context_data method'

        return context