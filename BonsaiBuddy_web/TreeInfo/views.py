# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import TreeInfo
from django.views import View, generic
from utils import get_object_or_404, user_has_any_perms
from .menu import TreeInfoMenuMixin

class IndexView(TreeInfoMenuMixin, generic.ListView):
    template_name = "TreeInfo/index.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        show_unpublished = user_has_any_perms(self.request.user, ["TreeInfo.change_content"])
        treeinfo = TreeInfo.objects
        print(show_unpublished)
        if not show_unpublished:
            treeinfo = treeinfo.filter(published=True)
        return treeinfo.order_by("name")

class DetailView(TreeInfoMenuMixin, View):
    model = TreeInfo
    template_name = "TreeInfo/detail.html"
    context_object_name = "tree_info"

    def get(self, request, pk):
        tree = get_object_or_404(self.model, name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: tree})
