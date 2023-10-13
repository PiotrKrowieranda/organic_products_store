"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from appproject.views import (AddCategoryView, EditCategoryView, CategoryListView, CategoryDetailsView, DeleteCategoryView, AddIngredientView, EditIngredientView,
                              IngredientDetailsView, IngredientListView, DeleteIngredientView, LoginFormView, LogoutView, Add_UserView,
                              Reset_passwordView, ProfileView, AddProductView, EditProductView, DeleteProductView,
                              ProductDetailView, ProductListView, SearchView, Order, CartView, YourOrdersView, OrderDetailsView, DeleteOrderView, ClearCartView, UpdateCartView)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout-url"),
    path('add_user/', Add_UserView.as_view(), name="register"),
    path('reset_password/', Reset_passwordView.as_view(), name="reset"),
    path('profile/', ProfileView.as_view(), name="profil"),

    path('', ProductListView.as_view(), name='index'),
    path('product/detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('product/edit/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('product/delete/<int:id>/', DeleteProductView.as_view(), name='delete_product'),

    path('category/add/', AddCategoryView.as_view(), name='add_category'),
    path('category/detail/<int:id>/', CategoryDetailsView.as_view(), name='category_details'),
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/edit/<int:id>/', EditCategoryView.as_view(), name='edit_category'),
    path('category/delete/<int:id>/', DeleteCategoryView.as_view(), name='delete_category'),

    path('ingredient/add/', AddIngredientView.as_view(), name='add_ingredient'),
    path('ingredient/edit/<int:ingredient_id>/', EditIngredientView.as_view(), name='edit_ingredient'),
    path('ingredient/details/<int:ingredient_id>/', IngredientDetailsView.as_view(), name='ingredient_details'),
    path('ingredient/list/', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/delete/<int:ingredient_id>/', DeleteIngredientView.as_view(), name='delete_ingredient'),

    path('search/', SearchView.as_view(), name='search_view'),

    path('cart/', CartView.as_view(), name='cart'),
    path('your_orders/', YourOrdersView.as_view(), name='your_orders'),
    path('clear_cart/', ClearCartView.as_view(), name='clear_cart'),
    path('update_cart/', UpdateCartView.as_view(), name='update_cart'),

    path('order/<int:order_id>/', OrderDetailsView.as_view(), name='order_details'),
    path('order/<int:order_id>/delete/', DeleteOrderView.as_view(), name='delete_order'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)