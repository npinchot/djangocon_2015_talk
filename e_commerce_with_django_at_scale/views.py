import logging
from django.core.cache import cache
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.template.loader import render_to_string
from django.views.generic import View
from models import Product

class CachedView(View):
    def _render_first_pass(self, request):
        # Try to load rendered first pass from cache
        rendered_template = cache.get(self.CACHE_KEY, None)

        if rendered_template is None:
            # Get first pass context vars, render template and save to cache
            logging.info('Rendering first pass template')
            context_vars = self.get_first_pass_context_vars(request)
            rendered_template = render_to_string(self.TEMPLATE, context_vars)
            cache.set(self.CACHE_KEY, rendered_template)

        return rendered_template

    def render(self, request):
        # Render first pass template
        first_pass_render = self._render_first_pass(request)

        # Set up template, get second pass context vars & render
        context_vars = self.get_second_pass_context_vars(request)
        template = Template(first_pass_render)
        output = template.render(RequestContext(request, context_vars))

        return HttpResponse(output)

    def get_first_pass_context_vars(self, request):
        return {}

    def get_second_pass_context_vars(self, request):
        return {}

class HomeView(CachedView):
    CACHE_KEY = 'HomeView'
    TEMPLATE = 'home.html'

    def get_first_pass_context_vars(self, request):
        products = Product.objects.all()

        return {'products': products}

    def get(self, request):
        return self.render(request)
