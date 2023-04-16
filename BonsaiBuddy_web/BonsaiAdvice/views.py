from django.shortcuts import render
from .menu import BonsaiAdviceMenuMixin
from django.views import generic
from .models import BonsaiTechnique

class IndexView(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = "BonsaiAdvice/index.html"
    context_object_name = "bonsai_techniques"

    def get_queryset(self):
        """Return the complete list of available trees."""
        return BonsaiTechnique.objects.filter(published=True).order_by("short_name")