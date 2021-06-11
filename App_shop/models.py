from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # admin panel a model er name set
    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    main_product_img = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    sort_description = models.CharField(max_length=265, verbose_name='sort_description')
    details_Description = models.TextField(verbose_name='details_Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_date']
