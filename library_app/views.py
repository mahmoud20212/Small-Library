from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def index(req):
    if req.method == 'POST':
        add_book = BookForm(req.POST, req.FILES)
        if add_book.is_valid():
            add_book.save()
        
        add_category = CategoryForm(req.POST)
        if add_category.is_valid():
            add_category.save()
    
    context = {
        'category': Category.objects.all(),
        'books': Book.objects.all(),
        'form': BookForm(),
        'formcat': CategoryForm(),
        'allbooks': Book.objects.filter(active=True).count(),
        'booksold': Book.objects.filter(status='sold').count(),
        'bookrental': Book.objects.filter(status='rental').count(),
        'bookavailble': Book.objects.filter(status='availble').count(),
    }
    return render(req, 'pages/index.html', context)

def books(req):
    serach = Book.objects.all()
    title = None
    if 'search_name' in req.GET:
        title = req.GET['search_name']
        if title:
            serach = serach.filter(title__icontains=title)
        
    context = {
        'category': Category.objects.all(),
        'books': serach,
        'formcat': CategoryForm(),
    }
    return render(req, 'pages/books.html', context)

def update(req, id):
    book_id = Book.objects.get(id=id)
    if req.method == 'POST':
        book_save = BookForm(req.POST, req.FILES, instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('/')
    else:
        book_save = BookForm(instance=book_id)
    
    context = {
        'form': book_save,
    }
    return render(req, 'pages/update.html', context)

def delete(req, id):
    book_delete = get_object_or_404(Book, id=id)
    if req.method == 'POST':
        book_delete.delete()
        return redirect('/')
    return render(req, 'pages/delete.html')
