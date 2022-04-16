from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse 
import uuid
from datetime import date
from django.contrib.auth.models import User 
from . import helpers

class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, Fantasy, etc.)')
    
    class Meta:
        verbose_name = "Genre"
    
    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField('Full Name', max_length=100, default="Unknown")
    country = models.CharField(max_length=100)
    date_of_birth = models.DateField('Birthdate',null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['name', 'country']

    def get_absolute_url(self):
        return reverse('author.detail', args=[str(self.id)])

    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField('Title', max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(
        'ISBN', 
        max_length=17,
        default='000-0-00-000000-0', 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Category, help_text='Select a genre for this book')
    lang = models.CharField('Language', default='English', max_length=100)
    edition = models.CharField('Edition', null=True, blank=True, max_length=100, help_text="Optional: You can specify the book edition")
    publisher = models.CharField('Publisher', null=True, blank=True, max_length=100, help_text="Optional: You can specify the book publisher ")    
    pub_date = models.CharField('Published', max_length=50, default="2021")
    summary = models.TextField(null=True, blank=True, max_length=1000, help_text='Enter a brief description of the book')
    
    
    class Meta:
        ordering = ['title', 'author']
            
    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book.detail', args=[str(self.id)])


class IssuedBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    issued_date = models.DateField('issued date', null=True, blank=True)
    expiry_date = models.DateField('due date', null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.expiry_date and date.today() > self.expiry_date:
            return True
        return False
    options = (
        ('m', 'MAINTENANCE'),
        ('o', 'LOANED'),
        ('a', 'AVAILABLE'),
        ('r', 'RESERVED'),
    )

    status = models.CharField(
        max_length=1,
        choices=options,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['issued_date','expiry_date']
        permissions = (("can_mark_returned", "Set book as returned"),)
        verbose_name_plural = "Catalog"

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    