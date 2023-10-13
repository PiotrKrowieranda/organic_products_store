import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from appproject.models import Product, CartItem, Order, Category, Ingredient
from django.test import RequestFactory
from django.http import Http404

# Utworzenie użytkownika testowego
@pytest.fixture
def user():
    # Tworzenie użytkownika testowego
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

# Utworzenie produktu testowego
@pytest.fixture
def product():
    # Tworzenie przykładowego produktu do testów
    product = Product.objects.create(name='Test Product', price=10.0, stock=50)
    return product

# Utworzenie elementu koszyka testowego
@pytest.fixture
def cart_item(user, product):
    # Tworzenie przykładowego elementu koszyka do testów
    cart_item = CartItem.objects.create(user=user, product=product, quantity=2, unit_price=product.price)
    return cart_item

# Utworzenie zamówienia testowego
@pytest.fixture
def order(user):
    # Tworzenie przykładowego zamówienia do testów
    order = Order.objects.create(user=user, total_amount=20.0, shipping_address='Test Address', phone_number='123-456-789')
    return order

# Utworzenie kategorii testowej
@pytest.fixture
def category():
    # Tworzenie przykładowej kategorii do testów
    category = Category.objects.create(category_name='Test Category')
    return category

# Utworzenie składnika testowego
@pytest.fixture
def ingredient():
    # Tworzenie przykładowego składnika do testów
    ingredient = Ingredient.objects.create(name='Test Ingredient')
    return ingredient

# Test widoku czyszczenia koszyka
@pytest.mark.django_db
def test_clear_cart_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania POST na widok "clear_cart"
    response = client.post(reverse('clear_cart'))
    # Oczekujemy przekierowania po wyczyszczeniu koszyka
    assert response.status_code == 302

# Test widoku zamówień użytkownika
@pytest.mark.django_db
def test_your_orders_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "your_orders"
    response = client.get(reverse('your_orders'))
    # Oczekujemy dostępu do widoku zamówień użytkownika
    assert response.status_code == 200

# Test widoku szczegółów zamówienia
@pytest.mark.django_db
def test_order_details_view(client, user, order):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "order_details" z argumentem "order.id"
    response = client.get(reverse('order_details', args=[order.id]))
    # Oczekujemy dostępu do widoku szczegółów zamówienia
    assert response.status_code == 200

# Test widoku listy kategorii
@pytest.mark.django_db
def test_category_list_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "category_list"
    response = client.get(reverse('category_list'))
    # Oczekujemy dostępu do widoku listy kategorii
    assert response.status_code == 200

# Test widoku szczegółów składnika
@pytest.mark.django_db
def test_ingredient_details_view(client, user, ingredient):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "ingredient_details" z argumentem "ingredient.id"
    response = client.get(reverse('ingredient_details', args=[ingredient.id]))
    # Oczekujemy dostępu do widoku szczegółów składnika
    assert response.status_code == 200

# Test widoku listy składników
@pytest.mark.django_db
def test_ingredient_list_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "ingredient_list"
    response = client.get(reverse('ingredient_list'))
    # Oczekujemy dostępu do widoku listy składników
    assert response.status_code == 200

#Test widoku listy koszyka
@pytest.mark.django_db
def test_cart_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "cart"
    response = client.get(reverse('cart'))
    # Oczekujemy dostępu do widoku listy koszyka
    assert response.status_code == 200

# Test widoku listy zamówień użytkownika
@pytest.mark.django_db
def test_your_orders_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "your_orders"
    response = client.get(reverse('your_orders'))
    # Oczekujemy dostępu do widoku listy zamówień użytkownika
    assert response.status_code == 200

# Test widoku czyszczenia koszyka
@pytest.mark.django_db
def test_clear_cart_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania POST na widok "clear_cart"
    response = client.post(reverse('clear_cart'))
    # Oczekujemy przekierowania po wyczyszczeniu koszyka
    assert response.status_code == 302


# Test widoku usuwania zamówienia
@pytest.mark.django_db
def test_delete_order_view(client, user, order):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania POST na widok "delete_order" z argumentem "order.id"
    response = client.post(reverse('delete_order', args=[order.id]))
    # Oczekujemy przekierowania po usunięciu zamówienia
    assert response.status_code == 302

# Test widoku wyszukiwania
@pytest.mark.django_db
def test_search_view(client, user):
    # Logowanie użytkownika
    client.force_login(user)
    # Wysyłanie żądania GET na widok "search_view"
    response = client.get(reverse('search_view'))
    # Oczekujemy dostępu do widoku wyszukiwania
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_product_view(client, admin_user):
    # Logowanie jako administrator (lub inny użytkownik z uprawnieniami do dodawania produktów)
    client.force_login(admin_user)
    # Wysyłanie żądania GET na widok "add_product"
    response = client.get(reverse('add_product'))
    # Oczekujemy dostępu do widoku dodawania produktu
    assert response.status_code == 200






