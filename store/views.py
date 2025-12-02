from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book

# Book List
def book_list(request, category_slug=None):
    category = None
    categories = Category.objects.all() 
    books = Book.objects.filter(available=True, stock__gt=0) 

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'books': books,
    }
    return render(request, 'store/list.html', context)

# Book Detail
def book_detail(request, category_slug, id, book_slug):
    book = get_object_or_404(Book, id=id, slug=book_slug, available=True, category__slug=category_slug)
    context = {
        'book': book,
    }
    return render(request, 'store/detail.html', context)

# Authentication
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) 
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form
    }
    return render(request, 'auth/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('book_list')

