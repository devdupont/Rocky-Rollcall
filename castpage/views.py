from django.shortcuts import render, get_object_or_404
from .models import Cast

# Create your views here.

def cast_home(request, slug: str):
    cast = get_object_or_404(Cast, slug=slug)
    return render(request, 'castpage/home.html', {'cast': cast})
