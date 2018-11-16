"""
Search views
"""

# django
# from django.db.models import Q
from django.views.generic.list import ListView
# from django.contrib.auth.models import User
# app
from castpage.models import Cast
from .forms import CastSearchForm

# def find_user_by_name(query_name: str):
#     """
#     """
#     qs = User.objects.all()
#     for term in query_name.split():
#         qs = qs.filter( Q(first_name__icontains = term) | Q(last_name__icontains = term))
#     return qs

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
        return Cast.objects.filter(name__trigram_similar=name)

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

    def post(self, request, *args, **kwargs):
        """
        Enables POST requests for form submit
        """
        return self.get(request, *args, **kwargs)
