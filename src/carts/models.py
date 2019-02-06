from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product


"""
django.conf.settings.AUTH_USER_MODEL vs django.contrib.auth.get_user_mdoel()
https://stackoverflow.com/questions/24629705/django-using-get-user-model-vs-settings-auth-user-model
"""
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            print(f"cart id {cart_id} exists")
            cart_obj = qs.first()
            if request.user.is_authenticated() and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
        else: 
            cart_obj = Cart.objects.new_cart(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.id
        return cart_obj, new_obj

    def new_cart(self, user=None):
        user_obj = None
        if user and user.is_authenticated():
            user_obj = user
        print("new cart created")
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    subtotal       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance,action, *args, **kwargs):
    if action.startswith("post") or action.startswith("pre"):
        print(action)
        products = instance.products.all()
        total=0
        for product in products:
            total += product.price
        print(total)
        if instance.subtotal != total:        
            instance.subtotal = total
            instance.save()
# def m2m_changed_cart_receiver(sender, instance,action, *args, **kwargs):
#     print(action)
#     print(instance.products.all())
#     print(instance.total)
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    # 8% tax?
    instance.total = float(instance.subtotal) * 1.08

pre_save.connect(pre_save_cart_receiver, sender=Cart)