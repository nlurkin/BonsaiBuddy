from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CreateForm
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
        return render(request, "BonsaiAdmin/index.html", self.menu_context)

# Create your views here.
class CreateTreeInfoFormView(AdminMenuMixin, PermissionRequiredMixin, FormView):
    permission_required = 'TreeInfo.change_content'

    template_name = 'BonsaiAdmin/create_treeinfo.html'
    form_class = CreateForm
    success_url = reverse_lazy("BonsaiAdmin:index")
    which_action = 'create'

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        top["which_action"] = self.which_action
        return top

    def form_valid(self, form):
        try:
            form.create()
        except NotUniqueError:
            messages.error(self.request, "Tree already exists in database.")
            return super().form_invalid(form)
        return super().form_valid(form)

class UpdateTreeInfoFormView(AdminMenuMixin, PermissionRequiredMixin, FormView):
    permission_required = 'TreeInfo.change_content'

    template_name = 'BonsaiAdmin/create_treeinfo.html'
    form_class = CreateForm
    success_url = reverse_lazy("BonsaiAdmin:index")
    which_action = 'update'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        tree = get_object_or_404(TreeInfo, name=context["pk"])
        form = self.form_class(initial=tree.to_mongo().to_dict())
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        top["which_action"] = self.which_action
        return top

    def form_valid(self, form):
        try:
            form.update()
        except NotUniqueError:
            messages.error(self.request, "Tree already exists in database.")
            return super().form_invalid(form)
        return super().form_valid(form)