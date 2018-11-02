"""
Search views
"""

# django
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
# app
from castpage.models import Cast
from .forms import CastSearchForm

class CastSearchListView(ListView):
    """
    Search and view Cast results
    """

    model = Cast
    paginate_by = 12
    context_object_name = 'casts'
    template_name = 'search/cast.html'

    def get_queryset(self) -> 'QuerySet':
        """
        Filter casts by name found in form POST or URL params
        """
        name = self.request.POST.get('name') or self.request.GET.get('name')
        if not name:
            return []
        return Cast.objects.filter(name__search=name) # pylint: disable=E1101

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = CastSearchForm(self.request.POST)
        else:
            context['form'] = CastSearchForm()
        return context

    # Enable POST requests for form submit
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
