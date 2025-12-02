from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Book
from .models import Cart, CartItem

def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('book').all()

    total_price = sum(item.get_total_price() for item in items)

    message = request.session.pop('cart_message', None)

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'message': message,
    }
    return render(request, 'cart/detail.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, book.stock))

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created_item = CartItem.objects.get_or_create(cart=cart, book=book)
    item.quantity = quantity
    item.save()

    messages.success(request, f'Đã thêm {quantity} "{book.title}" vào giỏ hàng.')

    return redirect('book_detail', category_slug=book.category.slug, id=book.id, book_slug=book.slug)

def cart_increase(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect("cart_detail")

def cart_decrease(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect("cart_detail")

@login_required
def cart_delete(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_detail")
