from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from store.models import Book
from .models import Cart, CartItem, Order, OrderItem

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

@login_required
def cart_delete(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_detail")

@login_required
def cart_update(request):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)

        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                try:
                    item_id = int(key.replace("quantity_", ""))
                    item = cart.items.get(id=item_id)
                    quantity = int(value)
                    quantity = max(1, min(quantity, item.book.stock))
                    item.quantity = quantity
                    item.save()
                except (ValueError, CartItem.DoesNotExist):
                    continue

    return redirect('cart_detail')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related('book').all()

    if not items.exists():
        messages.info(request, "Giỏ hàng đang trống.")
        return redirect('cart_detail')

    with transaction.atomic():
        total_price = sum(item.get_total_price() for item in items)

        order = Order.objects.create(user=request.user, total_price=total_price)

        for item in items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.get_discount_price()
            )
            item.book.stock -= item.quantity
            item.book.save()

        items.delete()

    messages.success(request, f"Đặt hàng thành công! Mã đơn hàng #{order.id}")
    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = Order.objects.prefetch_related('items__book').get(id=order_id, user=request.user)
    return render(request, 'cart/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__book').order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})
