
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponseNotFound
from .models import Ingredient, Product, Category, CartItem, Order
from .forms import (IngredientForm, EditIngredientForm, IngredientDetailsForm, DeleteIngredientForm, CategoryForm, ProductForm,
                    UserRegistrationForm, Reset_passwordForm, LoginForm, SearchForm, DeleteCategoryForm, DeleteProductForm, EditCategoryForm, OrderForm, CartItemForm, AddToCartForm, EditProductForm)

class CartView(LoginRequiredMixin, View):
    # Widok koszyka zakupów
    def get(self, request):
        # Pobranie przedmiotów w koszyku użytkownika
        cart_items = CartItem.objects.filter(user=request.user)
        order_form = OrderForm()
        total_price = sum(cart_item.subtotal() for cart_item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'order_form': order_form, 'total_price': total_price})

    def post(self, request):
        # Pobranie przedmiotów w koszyku użytkownika
        cart_items = CartItem.objects.filter(user=request.user)
        order_form = OrderForm(request.POST)

        if 'update_cart' in request.POST:  # Sprawdź, czy naciśnięto przycisk "Aktualizuj koszyk"
            for cart_item in cart_items:
                quantity_key = f'quantity_{cart_item.id}'
                new_quantity = int(request.POST.get(quantity_key, 1))  # Domyślnie 1 jeśli nie podano
                if 1 <= new_quantity <= cart_item.product.stock:  # Czy ilość jest poprawna
                    cart_item.quantity = new_quantity
                    cart_item.save()
                else:
                    # Wyświetl błąd
                    messages.error(request,
                                   f"Ilość produktu {cart_item.product.name} nie może być mniejsza niż 1 ani większa niż dostępna w magazynie ({cart_item.product.stock}).")
                    return redirect('cart')


        elif 'clear_cart' in request.POST:  # Sprawdź, czy naciśnięto przycisk "Wyczyść koszyk"
            CartItem.objects.filter(user=request.user).delete()
            return redirect('cart')

        if order_form.is_valid():
            # Pobieranie produktów w koszyku użytkownika
            user_cart_items = CartItem.objects.filter(user=request.user)
            user_cart_products = [cart_item.product for cart_item in user_cart_items]

            # Przetwarzanie zamówienia i zapis do bazy danych
            # Tutaj można utworzyć nowe zamówienie, obliczyć łączną kwotę, itp.
            total_amount = sum(cart_item.subtotal() for cart_item in user_cart_items)
            shipping_address = order_form.cleaned_data['shipping_address']
            phone_number = order_form.cleaned_data['phone_number']

            # walidacja ilości produktów w koszyku przed składaniem zamówienia
            for cart_item in user_cart_items:
                if cart_item.quantity > cart_item.product.stock:
                    messages.error(request,
                                   f"Ilość produktu {cart_item.product.name} nie może być większa niż dostępna w magazynie ({cart_item.product.stock}).")
                    return redirect('cart')

            # Rozpoczęcie transakcji bazodanowej
            with transaction.atomic():
                new_order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    shipping_address=shipping_address,
                    phone_number=phone_number
                )

                # Przypisanie produktów do zamówienia
                new_order.products.add(*user_cart_products)

                # Zmniejszenie stanu magazynowego produktów w koszyku
                for cart_item in user_cart_items:
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()

                # Usunięcie produktów z koszyka
                CartItem.objects.filter(user=request.user).delete()
                return redirect('your_orders')

        return render(request, 'cart.html', {'cart_items': cart_items, 'order_form': order_form})


class UpdateCartView(LoginRequiredMixin, View):
    # Widok aktualizacji koszyka
    def post(self, request):
        # Pobierz przedmioty w koszyku użytkownika
        cart_items = CartItem.objects.filter(user=request.user)

        if 'update_cart' in request.POST:
            for cart_item in cart_items:
                quantity_key = f'quantity_{cart_item.id}'
                new_quantity = int(request.POST.get(quantity_key, 1))  # Domyślnie 1, jeśli nie podano ilości
                if new_quantity > 0:
                    cart_item.quantity = new_quantity
                    cart_item.save()

        return redirect('cart')


class ClearCartView(LoginRequiredMixin, View):
    # Widok czyszczenia koszyka
    def post(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return redirect('cart')



class YourOrdersView(LoginRequiredMixin, View):
    # Widok zamówień użytkownika
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'your_orders.html', {'orders': orders})


class OrderDetailsView(LoginRequiredMixin, View):
    # Widok szczegółów zamówienia
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        # Pobieranie produktów z zamówienia
        products_in_order = order.products.all()

        # Pobieranie pozycji w koszyku związanego z danym zamówieniem
        cart_items = CartItem.objects.filter(user=request.user, product__in=products_in_order)

        return render(request, 'order_details.html', {'order': order, 'cart_items': cart_items})


class DeleteOrderView(LoginRequiredMixin, View):
    # permission_required = 'appproject.delete_order'

    # Widok usuwania zamówienia
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        # Przywracanie stanu magazynowego
        for cart_item in CartItem.objects.filter(user=request.user, product__in=order.products.all()):
            product = cart_item.product
            product.stock += cart_item.quantity
            product.save()

        order.delete()
        messages.success(request, f'Zamówienie nr {order_id} zostało usunięte.')

        return redirect('your_orders')


######################
class LoginFormView(View):
    # Widok logowania
    def get(self, request):
        # Tworzenie formularza uwierzytelniania i przekazanie danych z żądania
        f = LoginForm()
        # Pobierz URL 'next' z parametru GET lub pusty ciąg znaków, jeśli nie istnieje
        next_url = request.GET.get('next', '')

        # Przekazujemy formularz i 'next' jako kontekst do szablonu
        return render(request, "login-form.html", {'form': f, 'next': next_url})

    def post(self, request):
        # Tworzenie formularza uwierzytelniania i przekazanie danych z żądania
        form = LoginForm(request.POST)

        # Pobierz URL 'next' z parametru GET lub pusty ciąg znaków, jeśli nie istnieje
        next_url = request.GET.get('next', '')

        if form.is_valid():
            username = form.cleaned_data['login']
            passwd = form.cleaned_data['password']
            user = authenticate(username=username, password=passwd)

            if user is not None:
                login(request, user)

                if next_url:
                    # Przekieruj na 'next', jeśli istnieje
                    return redirect(next_url)
                else:
                    # Przekieruj na domyślny widok, jeśli nie ma 'next'
                    return redirect('index')

        # Jeśli formularz jest nieprawidłowy lub autentykacja nie powiodła się, wyświetl stronę logowania
        return render(request, "login-form.html", {'form': form, 'next': next_url})


class LogoutView(View):
    # Widok wylogowywania
    def get(self, request):
        logout(request)
        f = LoginForm()
        return render(request, "login-form.html", {'form': f})



class Add_UserView(View):
    # Widok dodawania użytkownika
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Tworzenie nowego użytkownika
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            messages.success(request, "Użytkownik został pomyślnie zarejestrowany.")
            # Przekierowanie na stronę logowania z komunikatem success
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})


class Reset_passwordView(View):
    # Widok resetowania hasła
    def get(self, request):
        # Tworzenie formularza uwierzytelniania i przekazanie danych z żądania
        form = Reset_passwordForm()
        # Przekazujemy formularz i 'next' jako kontekst do szablonu
        return render(request, "Reset_password.html", {'form': form})

    def post(self, request):
        # Tworzenie formularza uwierzytelniania i przekazanie danych z żądania
        form = Reset_passwordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password == password_confirm:
                user = request.user
                if user.is_authenticated:
                    user.set_password(password)
                    user.save()
                    messages.success(request, f'zmieniono hasło dla {request.user.username}')
                    return redirect('profil')

        return render(request, "Reset_password.html", {'form': form})


class ProfileView(LoginRequiredMixin, View):
    # Widok profilu użytkownika
    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'profile.html', context)


class AddCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # widok dodawania kategorii
    permission_required = 'appproject.add_category'

    def post(self, request):
        form = CategoryForm(request.POST)
        if Category.objects.filter(category_name=form.data['category_name']).exists():
            messages.error(request, "Taka kategoria już istnieje.")

        if form.is_valid():
            form.save()
            messages.success(request, "Dodano kategorię")
            return redirect('category_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Błąd w polu {form.fields[field].label}: {error}")
            messages.error(request, "Proszę poprawić błędy w formularzu.")
        return render(request, 'add_category.html', {'form': form})

    def get(self, request):
        # if not request.user.has_perm('appproject.add_category'):
        #     messages.error(request, "Strona dostępna tylko dla administratora.")
        #     return redirect('login')

        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})


class EditCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # Widok edycji kategorii
    permission_required = 'appproject.change_category'

    def post(self, request, id):
        category = get_object_or_404(Category, pk=id)
        form = EditCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect('category_list')

        return render(request, 'edit_category.html', {'form': form, 'category': category})

    def get(self, request, id):
        category = get_object_or_404(Category, pk=id)
        form = EditCategoryForm(instance=category)
        return render(request, 'edit_category.html', {'form': form, 'category': category})


class CategoryDetailsView(LoginRequiredMixin, View):
    # widok szczegółów kategorii
    def get(self, request, id):
        # Pobierz kategorię na podstawie identyfikatora 'id'
        category = get_object_or_404(Category, pk=id)

        # Pobierz produkty przypisane do danej kategorii, posortowane alfabetycznie
        products = Product.objects.filter(categories=category).order_by('name')


        return render(request, 'category_details.html', {'category': category, 'products': products})


class CategoryListView(LoginRequiredMixin, View):
    # widok listy kategorii
    def get(self, request):
        categories = Category.objects.all().order_by('category_name')
        return render(request, 'category_list.html', {'categories': categories})


class AddIngredientView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # widok dodawania sklądnika
    permission_required = 'appproject.add_ingredient'
    def get(self, request):
        form = IngredientForm()
        return render(request, 'add_ingredient.html', {'form': form})

    def post(self, request):

        form = IngredientForm(request.POST, request.FILES)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.image = request.FILES['image']
            ingredient.save()
            messages.success(request, "Dodano składnik")
            return redirect('add_ingredient')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Błąd w polu {form.fields[field].label}: {error}")
            messages.error(request, "Proszę poprawić błędy w formularzu.")
        return render(request, 'add_ingredient.html', {'form': form})


class EditIngredientView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'appproject.change_ingredient'


    def post(self, request, ingredient_id):

        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        form = EditIngredientForm(request.POST, request.FILES, instance=ingredient)

        if form.is_valid():
            form.save()
            return redirect('ingredient_list')

        return render(request, 'edit_ingredient.html',
                      {'form': form, 'ingredient': ingredient})

    def get(self, request, ingredient_id):

        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        form = EditIngredientForm(instance=ingredient)
        return render(request, 'edit_ingredient.html',
                      {'form': form, 'ingredient': ingredient})


class IngredientDetailsView(LoginRequiredMixin, View):
    def get(self, request, ingredient_id):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        return render(request, 'ingredient_details.html', {'ingredient': ingredient})


class IngredientListView(LoginRequiredMixin, View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        return render(request, 'ingredient_list.html', {'ingredients': ingredients})


class DeleteIngredientView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'appproject.delete_ingredient'
    def post(self, request, ingredient_id):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        form = DeleteIngredientForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm_delete']:
            ingredient.delete()
            return redirect('ingredient_list')

        return render(request, 'delete_ingredient.html', {'ingredient': ingredient, 'form': form})

    def get(self, request, ingredient_id):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        form = DeleteIngredientForm()
        return render(request, 'delete_ingredient.html', {'ingredient': ingredient, 'form': form})


class DeleteProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'appproject.delete_product'
    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = DeleteProductForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_delete']:
            product.delete()
            return redirect('index')

        return render(request, 'delete_product.html', {'product': product, 'form': form})

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = DeleteProductForm()
        return render(request, 'delete_product.html', {'product': product, 'form': form})


class DeleteCategoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    #widok kasowania kategorii
    permission_required = 'appproject.delete_category'
    def post(self, request, id):
        category = get_object_or_404(Category, pk=id)
        form = DeleteCategoryForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirm_delete']:
            category.delete()
            return redirect('category_list')

        return render(request, 'delete_category.html', {'category':category , 'form': form})

    def get(self, request, id):
        category = get_object_or_404(Category, pk=id)
        form = DeleteCategoryForm()
        return render(request, 'delete_category.html', {'category':category , 'form': form})


class AddProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    #widok dodawania produktu
    permission_required = 'appproject.add_product'

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.image = request.FILES['image']
            form.save()

            messages.success(request, "Dodano produkt")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Błąd w polu {form.fields[field].label}: {error}")
            messages.error(request, "Proszę poprawić błędy w formularzu.")

        return render(request, 'add_product.html', {'form': form})

    def get(self, request):
        if not request.user.has_perm('appproject.add_product'):
            messages.error(request, "Strona dostępna tylko dla administratora.")
            return redirect('login')

        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})


class EditProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # Widok edycji produktu
    permission_required = 'appproject.change_product'

    def post(self, request, product_id):  # Zmieniamy argument na 'product_id'
        product = get_object_or_404(Product, pk=product_id)
        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product_list')

        return render(request, 'edit_product.html', {'form': form, 'product': product})

    def get(self, request, product_id):  # Zmieniamy argument na 'product_id'
        product = get_object_or_404(Product, pk=product_id)
        form = EditProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})


class ProductListView(View):
    #widok listy produktów
    def get(self, request):
        products = Product.objects.all()
        cart_item_form = AddToCartForm()  # Dodaj formularz

        context = {
            "products": products,
            "cart_item_form": cart_item_form,  # Przekaż formularz do kontekstu szablonu
        }

        return render(request, "product_list.html", context)

    def post(self, request):
        # Obsługa dodawania produktów do koszyka
        cart_item_form = AddToCartForm(request.POST)

        if cart_item_form.is_valid():
            product_id = cart_item_form.cleaned_data['product_id']
            quantity = cart_item_form.cleaned_data['quantity']
            product = Product.objects.get(pk=product_id)

            # Sprawdź, czy produkt jest już w koszyku użytkownika
            existing_cart_item = CartItem.objects.filter(user=request.user, product=product).first()

            if existing_cart_item:
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
            else:
                cart_item = CartItem(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )
                cart_item.save()

            return redirect('cart')

        # Jeśli formularz nie jest prawidłowy, zwróć widok produktów z błędami walidacji

        products = Product.objects.all()

        context = {
            "products": products,
            "cart_item_form": cart_item_form,
        }

        return render(request, "product_list.html", context)


class ProductDetailView(LoginRequiredMixin, View):
    #widok szczegółów produktu
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        cart_item_form = CartItemForm()
        return render(request, "product_detail.html", {"product": product, "cart_item_form": cart_item_form})

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        cart_item_form = CartItemForm(request.POST)

        if cart_item_form.is_valid():
            quantity = cart_item_form.cleaned_data['quantity']
            # Sprawdź, czy produkt jest już w koszyku użytkownika
            existing_cart_item = CartItem.objects.filter(user=request.user, product=product).first()

            if existing_cart_item:
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
            else:
                cart_item = cart_item_form.save(commit=False)
                cart_item.user = request.user
                cart_item.product = product
                cart_item.unit_price = product.price  # Przypisz cenę jednostkową
                cart_item.save()

            return redirect('cart')

        return render(request, "product_detail.html", {"product": product, "cart_item_form": cart_item_form})


class SearchView(View):
    #Widok wyszukiewania produktu, kategorii składnika

    def get(self, request):
        form = SearchForm()
        return render(request, 'search_form.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']

            # Wyszukaj produkty i kategorie zawierające szukaną frazę w nazwie
            products = Product.objects.filter(name__icontains=search_query)
            categories = Category.objects.filter(category_name__icontains=search_query)
            ingredients = Ingredient.objects.filter(name__icontains=search_query)

            return render(request, 'search_results.html', {'products': products, 'categories': categories, 'ingredients': ingredients})

        return render(request, 'search_form.html', {'form': form})

