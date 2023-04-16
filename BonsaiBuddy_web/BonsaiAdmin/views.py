from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TreeInfoForm
from django.urls import reverse_lazy
from django.views.generic import View
from mongoengine.errors import NotUniqueError
from django.contrib import messages
from .menu import AdminMenuMixin
from TreeInfo.models import TreeInfo
from utils import get_object_or_404

class IndexView(AdminMenuMixin, PermissionRequiredMixin, View):
    permission_required = 'TreeInfo.change_content'

    def get(self, request):
        return render(request, "BonsaiAdmin/index.html", self.build_menu_context())

# Create your views here.
class TreeInfoFormView(AdminMenuMixin, PermissionRequiredMixin, FormView):
    permission_required = 'TreeInfo.change_content'

    template_name = 'BonsaiAdmin/create_treeinfo.html'
    form_class = TreeInfoForm
    success_url = reverse_lazy("BonsaiAdmin:index")

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        if "pk" in top:
            top["which_action"] = "update"
        else:
            top["which_action"] = "create"
        return top

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "pk" in context:
            tree = get_object_or_404(TreeInfo, name=context["pk"])
            form = self.form_class(initial={**tree.to_mongo().to_dict(), "update": True})
            form.fields["name"].widget.attrs["readonly"] = True
            context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        try:
            form.create_update()
        except NotUniqueError:
            messages.error(self.request, "Tree already exists in database.")
            return super().form_invalid(form)
        return super().form_valid(form)
