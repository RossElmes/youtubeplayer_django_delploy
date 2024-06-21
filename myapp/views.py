from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from myapp.models import Product, Order , OrderItem
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from .forms import AddProductForm ,AddToOrderForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.timezone import now

# Create your views here.
def place_order(request):
    products = Product.objects.all()
    order, created = Order.objects.get_or_create(customer=request.user, completed=False)
    order_items = order.items.all() 

    context = {
        'products': products,
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'myapp/place_order.html', {'prods': products, 'order': order,'order_items': order_items})

def product_list(request):
    products = Product.objects.all() 

    return render(request, 'myapp/product_list.html', {'prods': products})

def about(request):
    return render(request,'myapp/about.html',{'title':'Blog'})

@login_required
def add_product(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add products.")
        return redirect('place_order')  # Redirect to some appropriate page

    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('place_order')  # Redirect to the product list or some appropriate page
    else:
        form = AddProductForm()
    
    return render(request, 'myapp/addproduct.html', {'form': form})


@login_required
def delete_product(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete products.")
        return redirect('place_order')  # Redirect to some appropriate page

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('place_order')  # Redirect to the product list or some appropriate page

    return render(request, 'myapp/delete_product_confirm.html', {'product': product})


def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user, completed=False)

    order_item = order.items.filter(product=product).first()
    
    if order_item:
        # If product already in order, increment quantity
        order_item.quantity += 1
        order_item.save()
    else:
        # Otherwise, create a new OrderItem
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    return redirect('place_order')  # 

def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Example logic to confirm order (modify as per your application's business rules)
    if not order.completed:
        order.completed = True
        order.save()

        # Call update_total_amount method to update total_amount
        order.update_total_amount()

        # Redirect to order detail page or any other appropriate page
        return redirect('order_detail', order_id=order.id)
    else:
        # Order is already confirmed, handle this scenario (optional)
        return redirect('order_detail', order_id=order.id)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()  # Fetch order items associated with the order

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'myapp/order_detail.html', context)


def orders_today(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add products.")
        return redirect('place_order')  # Redirect to some appropriate page

    today = now().date()
    orders = Order.objects.filter(created_at__date=today)

    context = {
        'orders': orders,
    }
    return render(request, 'myapp/orders_today.html', context)


