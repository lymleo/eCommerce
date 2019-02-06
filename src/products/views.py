from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models.query import QuerySet
from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewMixin

# Create your views here.

class ProductFeaturedListView(ListView):
    queryset = Product.objects.all().featured
    template_name = "products/list.html"

    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.features()

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductFeaturedListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class ProductFeaturedDetailView(ObjectViewMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = "products/featured_detail.html"
    def get_queryset(self, *args, **kwargs):
        return Product.objects.features()

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductFeaturedDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all()

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset,
    }
    return render(request, 'products/list.html', context)


class ProductDetailSlugView(ObjectViewMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        # request = self.request
        slug = self.kwargs.get('slug')

        # instance = get_object_or_404(Product, slug=slug, active=True)
        # instance = Product.objects.get(slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not Found...")
        except Product.MultipleObjectsReturned:
            return Product.objects.filter(slug=slug, active=True).first()
        except:
            raise Http404("Uhmmmmm")

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)     
        return instance


class ProductDetailView(ObjectViewMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/detail.html'
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     # context['abc'] = 123
    #     return context

    # def get_object(self, *args, **kwargs) :
    #     # request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if not instance:
    #         raise Http404("Product not exist@@")
    #     return instance

    
    # acoording to method flow chart, get_queryset is prior to get_object, 
    # so disable get_object if want to use get_queryset

    def get_queryset(self, *args, **kwargs):
        # reqeust = self.request
        pk = self.kwargs.get('pk')
        # return Product.objects.all()
        return Product.objects.filter(pk=pk)

def product_detail_veiw(request, pk = None, *args, **kwargs):
    # queryset = Product.objects.all()
    # instance = Product.objects.get(pk = pk)
    # instance = get_object_or_404(Product, pk = pk)

    # try:
    #     id = pk
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("product not exist")
    # except:
    #     print('huh?')

    instance = Product.objects.get_by_id(pk)
    if not instance:
        raise Http404("product not exist!!!!!!!!!!")
    # print("Instance is: ", instance)
    # qs = Product.objects.filter(pk = pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("product not exist")


    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)

