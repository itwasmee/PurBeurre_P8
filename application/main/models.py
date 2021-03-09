from pprint import pprint
from django.db import models
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return 'store: ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return 'category: ' + self.name


class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    description = models.TextField()
    url = models.CharField(max_length=200)
    store = models.ManyToManyField(Store)
    popularity = models.IntegerField()
    category = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return 'product: ' + self.name

    def retrieve_product(request):
        vector = SearchVector('name')
        query = SearchQuery(request)
        winner = Product.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')[0]
        if winner:
            return winner


class History(models.Model):
    page_number = models.IntegerField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
