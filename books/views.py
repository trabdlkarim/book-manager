from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, IssuedBook, Category
from .helpers import get_expiry_date
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ReserveBookForm

def home(request):
    # Generate counts of some of the main objects
    num_books = IssuedBook.objects.all().count()

    # Available books (status = 'a')
    num_books_available = IssuedBook.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genres = Category.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_instances_available': num_books_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits
    }
    
    return render(request, 'catalog/welcome.html', context)

def profile(request):
    context = {
        'message' : 'This is the catalog current user profile',
    }
    return render(request, 'catalog/profile.html', context)

def index(request):
    context = {
        'message' : 'This is catalog book index page',
    }
    return render(request, 'catalog/index.html', context)

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 50

class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    template_name = 'catalog/author_list.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    login_url = 'login'
    model = IssuedBook
    template_name ='catalog/user_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return IssuedBook.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('expiry_date')

def borrow_book_from_catalog(request, pk):
     book_instance = get_object_or_404(IssuedBook, pk=pk)
     
     if request.method == 'POST':
        if book_instance.status == 'a':
             book_instance.issued_date = datetime.now()
             book_instance.expiry_date =  get_expiry_date()
             book_instance.status = 'o'
             book_instance.borrower = request.user
             book_instance.save()
        
     return HttpResponseRedirect(reverse('books.borrowed'))

def reserve_book_from_catalog(request, pk):
    book_instance = get_object_or_404(IssuedBook, pk=pk)

    if request.method == 'POST':

        form = ReserveBookForm(request.POST)

        if form.is_valid() and book_instance.status == 'a':
            book_instance.issued_date = form.cleaned_data['start_date']
            book_instance.expiry_date = form.cleaned_data['start_date'] + timedelta(weeks=3)
            book_instance.status = 'r'
            book_instance.borrower = request.user
            book_instance.save()
            
            return HttpResponseRedirect(reverse('books.borrowed') )

    elif book_instance.status == 'a':
        proposed_date = datetime.today() + timedelta(weeks=3)
        form = ReserveBookForm(initial={'start_date': proposed_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/reserve_catalog_book.html', context)
    
    else:
        return HttpResponseRedirect(reverse('books.borrowed'))
         