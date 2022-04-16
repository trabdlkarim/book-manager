from django.contrib import admin
from .models import Author, Category, Book, IssuedBook


admin.site.register(Category)

class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book
    
# Define the admin class
# Register the admin class with the associated model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
     list_display = ('name', 'country', 'date_of_birth', 'date_of_death')
     fields = ['name', 'country', ('date_of_birth', 'date_of_death')]
     inlines = [BooksInline]


class IssuedBooksInline(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = IssuedBook 
    
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [IssuedBooksInline]

# Register the Admin classes for IssuedBook using the decorator
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'issued_date', 'expiry_date', 'id')
    list_filter = ('status', 'issued_date', 'expiry_date')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'issued_date', 'expiry_date', 'borrower')
        }),
    )