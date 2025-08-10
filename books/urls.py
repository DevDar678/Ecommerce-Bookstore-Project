
from django.urls import path
from . import views
from .views import BooksListView, BooksDetailView, BookCheckoutView, mybooks_by_category, SearchResultsListView

urlpatterns = [
    path('', views.index, name="list"),
    path('books/', BooksListView.as_view(), name='mybooks'),
    path('books/category/<slug:category_slug>/', views.mybooks_by_category, name='mybooks_by_category'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', BookCheckoutView.as_view(), name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name='checkout'),

    path('<int:book_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('orders/', views.order_list, name='order_list'), 

    path('checkout/selected/', views.checkout, name='checkout_selected'),
    path('cart/action/', views.cart_action, name='cart_action'),
  

]

