# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import TreeInfo
from django.views import View, generic
from utils import get_object_or_404

class IndexView(generic.ListView):
    template_name = "TreeInfo/index.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        return TreeInfo.objects.filter(published=True).order_by("name")

class DetailView(View):
    model = TreeInfo
    template_name = "TreeInfo/detail.html"
    context_object_name = "tree_info"

    def get(self, request, pk):
        question = get_object_or_404(self.model, name=pk)
        return render(request, self.template_name, {self.context_object_name: question})
