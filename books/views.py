from django.shortcuts import get_object_or_404, render, redirect 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from .models import Book, Order, CashOnDeliveryOrder, Cart, CartItem, Category
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.contrib import messages


def index(request):
    return render(request, "list.html")


class BooksListView(ListView):
    model = Book
    template_name = 'mybooks.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def mybooks_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    books = Book.objects.filter(category=category)
    print(f"Category: {category.name}")
    print(f"Books: {books}")
    return render(request, 'mybooks.html', {
        'books': books,
        'category': category.name
    })



class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
	model = Book
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return Book.objects.filter(
		Q(title__icontains=query) | Q(author__icontains=query)
		)

class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'login'

from django.views import View  # Add this import at the top

class BookCheckoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'checkout.html', {'object': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        phone_number = request.POST.get("phone_number")

        # Save the order
        order = CashOnDeliveryOrder.objects.create(
            name=name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone_number=phone_number
        )

        return render(request, "order_success.html", {"order": order})


def checkout(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        phone_number = request.POST.get("phone_number")

        # Save the order to the database
        order = CashOnDeliveryOrder.objects.create(
            name=name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone_number=phone_number
        )
        
        return render(request, "order_success.html", {"order": order})

        
    return render(request, "checkout.html")


 

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    # Get or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Retrieve all items in the cart

    return render(request, 'cart_detail.html', {'cart': cart, 'cart_items': cart_items})


@login_required
def cart_action(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        action = request.POST.get("action")
        cart = Cart.objects.get(user=request.user)

        if action == "delete":
            if selected_ids:
                CartItem.objects.filter(id__in=selected_ids, cart=cart).delete()
            return redirect('cart_detail')

        elif action == "buy":
            if not selected_ids:
                # If no items selected, select all
                selected_items = cart.items.all()
                selected_ids = [str(item.id) for item in selected_items]
            else:
                selected_items = CartItem.objects.filter(id__in=selected_ids, cart=cart)

            # Check stock availability
            out_of_stock = []
            for item in selected_items:
                if not item.book.book_available:
                    out_of_stock.append(item.book.title)

            if out_of_stock:
                messages.error(request, f"These books are out of stock: {', '.join(out_of_stock)}")
                return redirect('cart_detail')

            request.session['selected_cart_items'] = selected_ids
            # request.session['cart_total'] = str(sum(item.get_total() for item in selected_items))
            return redirect('checkout_selected')

    return redirect('cart_detail')       


def order_list(request):
    orders = Order.objects.all().order_by('-created')
    cod_orders = CashOnDeliveryOrder.objects.all().order_by('-created_at')
    return render(request, 'order_list.html', {
        'orders': orders,
        'cod_orders': cod_orders
    })



