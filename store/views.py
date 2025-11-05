from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem, SubCategory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from typing import cast

SORT_OPTIONS = {
    "newest": "-created_at",
    "price-asc": "price",
    "price-desc": "-price",
}

def home(request):
    try:
        featured_products = Product.objects.filter(is_featured=True)[:4]
        categories = Category.objects.all()
        context = {
            'featured_products': featured_products,
            'categories': categories
        }
    except ObjectDoesNotExist:
        # Fallback if models aren't created yet
        context = {
            'featured_products': [],
            'categories': []
        }

    return render(request, 'store/home.html', context)

'''def shop(request, category_slug=None):
    #Shows all products OR products in a single category
    active_category = None

    if category_slug:
        # get chosen category or 404 if wrong slug
        active_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=active_category)
    else:
        products = Product.objects.all()

    context = {
        "categories": Category.objects.all(),
        "products": products,
        "active_category": active_category,
    }
    
    return render(request, 'store/shop.html', context)

def category_view(request, slug):
    active_category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=active_category)
    #categories = Category.objects.all()

    return render(request, 'store/shop.html', {
        'products': products,
        'categories': Category.objects.all(),
        'active_category': active_category,
    })'''

def shop(request, category_slug=None):
    active_category = None
    active_sub = None

    # start with the base queryset
    products_qs = Product.objects.all()

    # category filter
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products_qs = products_qs.filter(category=active_category)
    
    # sub‑category filter
    sub_slug = request.GET.get("sub")
    if sub_slug:
        active_sub = get_object_or_404(SubCategory, slug=sub_slug, category=active_category)
        products_qs = products_qs.filter(subcategory=active_sub)

    # ------- sort -------
    sort_key = request.GET.get("sort", "newest")
    products_qs = products_qs.order_by(SORT_OPTIONS.get(sort_key, "-created_at"))

    # paginate the _filtered_ queryset
    paginator = Paginator(products_qs, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # gather sub‑categories for chips
    subcategories = SubCategory.objects.filter(category=active_category) if active_category else []

    context = {
        "products": page_obj.object_list, 
        "page_obj": page_obj,
        "has_next": page_obj.has_next(),
        "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
        "categories": Category.objects.all(),
        "active_category": active_category,
        "active_sub": active_sub,
        "subcategories": subcategories,
        "product_count": products_qs.count(),
        "sort_key": sort_key,
    }    
    return render(request, "store/shop.html", context)


def category_view(request, slug):
    return shop(request, category_slug=slug)   # reuse same logic

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    return render(request, 'store/cart.html', {
        'cart': cart
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )

    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity += quantity
    cart_item.save()
    
    return redirect('cart')

def wishlist(request):
    return render(request, "store/wishlist.html")

@require_POST
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))

    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()

    return redirect('cart')

# Handle the checkout process:
# 1. Display checkout form (GET request)
# 2. Process order submission (POST request)
@login_required
def checkout(request):
    # Get current user's cart or return 404
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST':
        # Process payment here and Create order
        order = Order.objects.create(
            user = request.user,
            total = cart.total_price,
            status = 'P'
        )
        
        # Move cart items to order
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order = order,
                product = cart_item.product,
                quantity = cart_item.quantity,
                price = cart_item.product.price
            )
        
        # Clear cart
        cart.cart_items.all().delete()
        
        return redirect('order_confirmation', order_id=order.id) # type: ignore

    return render(request, 'store/checkout.html', {
        'cart': cart
    })

# Display order confirmation page for a completed order.
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

def dashboard(request):
    return render(request, 'store/dashboard.html')

def search(request):
    return render(request, 'store/search.html')

def contact(request):
    return render(request, 'store/contact.html')

#Authenticate views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'store/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def product_api(request, pk):
    try:
        product: Product = get_object_or_404(Product, pk=pk)
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "price_display": f"₵{product.price:.2f}",
            "slug": product.slug,
            "image": product.image.url if product.image else "/static/images/default.jpg"
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)





