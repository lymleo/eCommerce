from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product

class SearchProductView(ListView):
    queryset = Product.objects.all()
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query:
            return Product.objects.search(query)
        print("no condition is given")
        return Product.objects.features()
        '''
            __icontains = field contains this
            __iexact = field is extacly this
        '''