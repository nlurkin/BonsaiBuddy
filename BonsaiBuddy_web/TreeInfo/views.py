# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import TreeInfo
from django.views import View, generic
from utils import get_object_or_404
from .menu import TreeInfoMenuMixin

class IndexView(TreeInfoMenuMixin, generic.ListView):
    template_name = "TreeInfo/index.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        return TreeInfo.objects.filter(published=True).order_by("name")

class DetailView(TreeInfoMenuMixin, View):
    model = TreeInfo
    template_name = "TreeInfo/detail.html"
    context_object_name = "tree_info"

    def get(self, request, pk):
        tree = get_object_or_404(self.model, name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: tree})
