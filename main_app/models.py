from django.db import models
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Func, Value, FloatField
from collections import defaultdict
from django.db.models import Q
from django.contrib.auth.models import User


class ProductManager(models.Manager):
    def get_sales_by_id(self, shop_id):
        return self.filter(
            shop_id=shop_id,
            last_price__isnull=False
        )

    def fuzzy_search_grouped_by_shop(self, query, threshold=0.2):
        products = (
            self.get_queryset()
            .annotate(
                similarity=TrigramSimilarity('name', Value(query))
            )
            .filter(Q(similarity__gt=threshold) | Q(name__icontains=query))
            .order_by('-similarity')
            .select_related('shop')
        )

        from collections import defaultdict
        grouped = defaultdict(list)
        for product in products:
            grouped[product.shop.name].append(product)

        return grouped

class Shop(models.Model):
    name = models.CharField(max_length=100)
    number_products = models.IntegerField()


class Product(models.Model):
    price = models.FloatField()
    last_price = models.FloatField(null=True)
    name = models.CharField(max_length=1000)
    image = models.URLField()
    weight = models.CharField(max_length=50)
    link = models.URLField(null=True)
    card_sale = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,default=1)

    objects = ProductManager()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='profile',
                                db_index=True)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
