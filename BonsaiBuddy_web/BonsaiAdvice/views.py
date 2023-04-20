from django.shortcuts import render
from .menu import BonsaiAdviceMenuMixin
from django.views import generic, View
from .models import BonsaiTechnique, BonsaiObjective
from utils import get_object_or_404

class IndexView(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = "BonsaiAdvice/index.html"
    context_object_name = "bonsai_techniques"

    def get_queryset(self):
        """Return the complete list of available trees."""
        return BonsaiTechnique.objects.filter(published=True).order_by("short_name")

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        top["bonsai_techniques"] = BonsaiTechnique.objects.filter(published=True).order_by("short_name")
        top["bonsai_objectives"] = BonsaiObjective.objects.filter(published=True).order_by("short_name")
        return top

class TechniqueView(BonsaiAdviceMenuMixin, View):
    model = BonsaiTechnique
    template_name = "BonsaiAdvice/detail_technique.html"
    context_object_name = "technique"

    def get(self, request, pk):
        obj_instance = get_object_or_404(self.model, short_name=pk)
        return render(request, self.template_name, {**self.build_menu_context(), self.context_object_name: obj_instance})
