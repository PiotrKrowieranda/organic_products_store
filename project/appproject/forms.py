from django import forms
from .models import Ingredient, Category, Product, Order, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Formularz dodawania lub edycji składnika
class IngredientForm(forms.ModelForm):
    """
    Formularz dodawania lub edycji składnika.
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


    def clean_name(self):
        # Walidacja nazwy składnika
        name = self.cleaned_data.get('name')

        # Sprawdzenie, czy nazwa nie jest pusta
        if not name:
            raise ValidationError("To pole jest wymagane.")

        # Sprawdzenie, czy składnik o takiej nazwie już istnieje
        if Ingredient.objects.filter(name=name).exists():
            raise ValidationError("Taki składnik już istnieje.")

        return name


    def clean_description(self):
        # Walidacja opisu składnika
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError("Pole opisu jest wymagane.")
        return description

# Formularz edycji składnika
class EditIngredientForm(forms.ModelForm):
    """
    Formularz edycji składnika.
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    # Nadpisana walidacja nazwy składnika
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("To pole jest wymagane w Edycji.")

        return name

# Formularz do wyświetlania szczegółów składnika (tylko do odczytu)
class IngredientDetailsForm(forms.ModelForm):
    """
    Formularz do wyświetlania szczegółów składnika (tylko do odczytu).
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'readonly': True}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'readonly': True}),
        }

# Formularz potwierdzenia usunięcia składnika
class DeleteIngredientForm(forms.Form):
    """
    Formularz potwierdzenia usunięcia składnika.
    """
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Potwierdzam usunięcie składnika',
    )

class DeleteCategoryForm(forms.Form):
    """
    Formularz potwierdzenia usunięcia kategorii.
    """
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Potwierdzam usunięcie kategorii',
    )

class DeleteProductForm(forms.Form):
    """
    Formularz potwierdzenia usunięcia produktu.
    """
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Potwierdzam usunięcie produktu',
    )


class CategoryForm(forms.ModelForm):
    """
    Formularz dodawania kategorii.
    """
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),  # Pole kategorii z wyglądem formularza Bootstrap
        }

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        if not category_name:
            raise ValidationError("To pole jest wymagane.")
        if Category.objects.filter(category_name=category_name).exists():
            raise ValidationError("Taka kategoria już istnieje.")
        return category_name


class EditCategoryForm(forms.ModelForm):
    """
    Formularz edycji kategorii.
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'vat', 'stock', 'categories', 'ingredients', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),  # Dodany widget dla pola 'image'
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        vat = cleaned_data.get('vat')
        stock = cleaned_data.get('stock')
        categories = cleaned_data.get('categories')
        ingredients = cleaned_data.get('ingredients')

        if not (name and description and price and vat and stock and categories and ingredients):
            raise ValidationError("Wszystkie pola są wymagane.")

        if not categories:
            raise ValidationError("Wybierz przynajmniej jedną kategorię.")

        if not ingredients:
            raise ValidationError("Wybierz przynajmniej jeden składnik.")

        return cleaned_data


class ProductForm(forms.ModelForm):
    """
    Formularz dodawania lub edycji produktu.
    """


    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'vat', 'stock', 'categories', 'ingredients', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),  # Dodany widget dla pola 'image'
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        vat = cleaned_data.get('vat')
        stock = cleaned_data.get('stock')
        categories = cleaned_data.get('categories')
        ingredients = cleaned_data.get('ingredients')

        if not (name and description and price and vat and stock and categories and ingredients):
            raise ValidationError("Wszystkie pola są wymagane.")

        if Product.objects.filter(name=name).exists():
            raise ValidationError("Taki produkt już istnieje.")

        if not categories:
            raise ValidationError("Wybierz przynajmniej jedną kategorię.")

        if not ingredients:
            raise ValidationError("Wybierz przynajmniej jeden składnik.")

        return cleaned_data


class UserRegistrationForm(forms.Form):
    """
    Formularz rejestracji użytkownika.
    """

    login = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_login(self):
        login = self.cleaned_data.get('login')

        if User.objects.filter(username=login).exists():
            raise ValidationError("Login jest już zajęty.")
        if not login:
            raise forms.ValidationError("To pole jest wymagane.")

        return login

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Hasła nie są identyczne.")
        if not password and password_confirm:
            raise forms.ValidationError("To pole jest wymagane.")


class Reset_passwordForm(forms.Form):
    """
    Formularz resetowania hasła użytkownika.
    """

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self):
        cleaned_data = super().clean() # wykonuje proces walidacji w klasie nadrzędnej (czyli klasie forms.Form), a następnie umieszcza wynik w słowniku cleaned_data.

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Hasła nie są identyczne.")
        if not password and password_confirm:
            raise forms.ValidationError("To pole jest wymagane.")


class LoginForm(forms.Form):
    """
    Formularz logowania użytkownika.
    """

    login = forms.CharField(label="Login",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # next = forms.CharField(widget=forms.HiddenInput(), required=False)

class SearchForm(forms.Form):
    """
    Formularz wyszukiwania.
    """

    search_query = forms.CharField(label='Szukaj', max_length=100)


class OrderForm(forms.ModelForm):
    """
    Formularz zamówienia.
    """

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']


class CartItemForm(forms.ModelForm):
    """
    Formularz przedmiotu w koszyku.
    """

    class Meta:
        model = CartItem
        fields = ['quantity']
        labels = {'quantity': 'Ilość'}
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Podaj ilość', 'min': '1'}),
        }

class AddToCartForm(forms.Form):
    """
    Formularz dodawania do koszyka.
    """

    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'quantity-input'}))
    product_id = forms.IntegerField(widget=forms.HiddenInput())
