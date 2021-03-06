from random import randint
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from ecommerce.utils import unique_slug_generator

# Create your models here.

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_imgae_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = randint(1, 39102093122)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}/'

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                   Q(description__icontains=query) |
                   Q(price__iexact=query) |
                   Q(tag__title__icontains=query)
                   )
        # Q=(tag__name__icontains=query)
        return self.filter(lookups).distinct()

# extends from models Manager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)
    
    def all(self):
        return self.get_queryset().active()
    
    def features(self):
        return self.get_queryset().filter(featured=True)
            
    def get_by_id(self, id):
        qs =  self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title = models.CharField(max_length=120) 
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to=upload_imgae_path, blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    objects = ProductManager()

    def get_absolute_url(self):
        # return f"/products/{self.slug}"
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
        
    def __unicode__(self):
        return self.title
    
    @property
    def name(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)