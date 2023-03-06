import datetime

from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from .forms import RenewBookForm
from .models import Book, Author, BookInstance


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


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class BookListView(generic.ListView):
    models = Book
    paginate_by = 10

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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user)
                .filter(status__exact='o')
                .order_by('due_back'))


class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'

    permission_required = ('catalog.can_mark_returned',)

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author