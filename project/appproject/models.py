from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Ingredient(models.Model):
    """
    Model reprezentujący składnik.
    """
    name = models.CharField(max_length=128)
    description = models.TextField(default='Brak opisu')
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Model reprezentujący kategorię produktu.
    """
    category_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        """
        Nadaje slug na podstawie category_name, jeśli slug jest pusty.
        """
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

class Product(models.Model):
    """
    Model reprezentujący produkt.
    """
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.IntegerField()
    categories = models.ManyToManyField(Category)
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    Model reprezentujący zamówienie.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name='orders', blank=True)

    def __str__(self):
        return f"Order by {self.user.username} on {self.order_date}"

class CartItem(models.Model):
    """
    Model reprezentujący przedmiot w koszyku.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def subtotal(self):
        """
        Oblicza wartość przedmiotu w koszyku.
        """
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"
