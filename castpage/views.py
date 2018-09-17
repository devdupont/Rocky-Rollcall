from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PageSectionForm
from .models import Cast, PageSection

# Create your views here.

def cast_home(request, slug: str):
    cast = get_object_or_404(Cast, slug=slug)
    return render(request, 'castpage/home.html', {'cast': cast})

@login_required
def cast_section_new(request, slug: str):
    cast = get_object_or_404(Cast, slug=slug)
    if request.method == 'POST':
        form = PageSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm()
    return render(request, 'castpage/section_edit.html', {'cast': cast, 'form': form})

@login_required
def cast_section_edit(request, slug: str, pk: int):
    cast = get_object_or_404(Cast, slug=slug)
    section = get_object_or_404(PageSection, pk=pk)
    print(section)
    if request.method == 'POST':
        form = PageSectionForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm(instance=section)
    return render(request, 'castpage/section_edit.html', {'cast': cast, 'form': form})

@login_required
def cast_section_remove(request, slug: str, pk: int):
    cast = get_object_or_404(Cast, slug=slug)
    section = get_object_or_404(PageSection, pk=pk)
    section.delete()
    return redirect('cast_home', slug=cast.slug)
