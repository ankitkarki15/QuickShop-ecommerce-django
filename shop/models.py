from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
# User model that extends AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=10, blank=True, null=True) 
    address = models.TextField(blank=True, null=True)

    # String representation of the User object (by default, username is returned)
    def __str__(self):
        return self.username  
    
    
class Product(models.Model):
    name = models.CharField(max_length=255) 
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField() 
    image = models.ImageField(upload_to='products_image/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name  
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)  # To mark default shipping/billing address

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
        
class Order(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the user who made the order
        shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="shipping_orders")
        product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Reference to the Product model
        quantity = models.PositiveIntegerField()  # Quantity of the product ordered
        price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of a single unit of the product
        order_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total order price (calculated field)
        created_at = models.DateTimeField(auto_now_add=True)  # Date and time the order was created
        updated_at = models.DateTimeField(auto_now=True)  # Date and time the order was last updated

        def save(self, *args, **kwargs):
            # Calculate order_total before saving the order
            self.order_total = self.price * self.quantity
            super().save(*args, **kwargs)  # Save the order with the calculated order_total

        def __str__(self):
           return f"Order #{self.id} by {self.user.username}"
       
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reviewer (assuming User model exists)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()  # Detailed review
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating 1-5
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated

    # Optional: Link review to a product, service, or other model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Review by {self.user} - Rating: {self.rating}/5"
