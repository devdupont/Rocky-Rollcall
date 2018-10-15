"""
View logic for cast page
"""

# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
# Other apps
from castadmin.forms import CastForm
from events.views import EventListView
# This app
from .models import Cast

@login_required
def cast_new(request):
    """
    Create a new cast
    """
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES)
        if form.is_valid():
            cast = form.save()
            cast.managers.add(request.user.profile)
            cast.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = CastForm()
    return render(request, 'castadmin/cast_edit.html', {'form': form})

def cast_home(request, slug: str):
    """
    Renders the cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    return render(request, 'castpage/home.html', {
        'cast': cast,
        'show_management': cast.is_manager(request.user),
        'tinylist': True,
    })

class CastEvents(EventListView):
    """
    Pagination view for future cast events
    """

    template_name = 'castpage/event_list.html'
    paginate_by = 2

    def get_queryset(self) -> ['Event']:
        """
        Filter queryset based on cast events
        """
        cast = get_object_or_404(Cast, slug=self.kwargs['slug'])
        return cast.future_events

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        cast = get_object_or_404(Cast, slug=self.kwargs['slug'])
        context['cast'] = cast
        context['show_cast'] = False
        context['show_management'] = cast.is_manager(self.request.user)
        return context
