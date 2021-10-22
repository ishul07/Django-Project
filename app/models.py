from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# STATE_CHOICES = (('Haryana', 'Haryana'), ('Delhi', 'Delhi'), ('Punjab', 'Punjab'),
#                  ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu & Kashmir', 'Jammu & Kashmir'))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()

    state = models.CharField(max_length=40)
    country = models.CharField(max_length=40, default='India')
    phone = models.CharField(max_length=10, default='')

    def __str__(self):
        return str(self.id)


# CATEGORY_CHOICES = (('Bedsheet', 'Bedsheet'),
#                     ('Pillow', 'Pillow'), ('Towel', 'Towel'))


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.CharField(max_length=2000)
    category = models.CharField(max_length=40)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price


STATus_CHOICES = (('Accepted', 'Accepted'), ('Delivered', 'Delivered'),
                  ('Cancel', 'Cancel'), ('Packed', 'Packed'), ('On the Way', 'On the Way'))


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATus_CHOICES,
                              max_length=30, default='Pending')

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
# Create your models here.
