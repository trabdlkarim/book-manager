from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('user/profile/', views.profile, name='profile'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book.detail'),
    path('books/borrowed/', views.LoanedBooksByUserListView.as_view(), name='books.borrowed'),
    path('book/<uuid:pk>/borrow/', views.borrow_book_from_catalog, name='book.borrow'),
    path('book/<uuid:pk>/reserve/', views.reserve_book_from_catalog, name='book.reserve'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(), name='author.detail'),
]