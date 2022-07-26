from django.db import models


class User(models.Model):
    username = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    birthday = models.DateField()

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f'{self.name} - ${self.price}'


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('product', 'order'), name='once_product_per_order')
        ]


class Order(models.Model):
    order_id = models.IntegerField(unique=True, null=False, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through=OrderProduct)

    def total(self):
        return self.objects.aggregate(
            total=models.Sum(models.F('orderproduct__quantity') * models.F('product__price'))
        )['total']

    def __str__(self):
        return f'{self.order_id} - ${self.total()}'
