from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

class PhotoGridView(ListView):
    """
    Pagination view for Photo list
    """

    paginate_by = 12
    context_object_name = 'photos'
