from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TreeInfoForm, BonsaiTechniqueForm, BonsaiObjectiveForm, BonsaiWhenForm
from django.urls import reverse_lazy
from django.views.generic import View
from mongoengine.errors import NotUniqueError
from django.contrib import messages
from .menu import AdminMenuMixin
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen
from utils import get_object_or_404, user_has_any_perms

class IndexView(AdminMenuMixin, PermissionRequiredMixin, View):
    permission_required = ['TreeInfo.change_content', "BonsaiAdvice.change_content"]

    def has_permission(self):
        return user_has_any_perms(self.request.user, self.permission_required)

    def get(self, request):
        return render(request, "BonsaiAdmin/index.html", self.build_menu_context(request))

class MyFormView(AdminMenuMixin, PermissionRequiredMixin, FormView):
    success_url = reverse_lazy("BonsaiAdmin:index")
    template_name = 'BonsaiAdmin/object_admin_form.html'

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        if "pk" in top:
            top["rev_url"] = f"BonsaiAdmin:{self.url_update_name}"
        else:
            top["rev_url"] = f"BonsaiAdmin:{self.url_create_name}"
        return top

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "pk" in context:
            kwargs = {self.index_name: context["pk"]}
            obj_instance = get_object_or_404(self.object_class, **kwargs)
            form = self.form_class(initial={**obj_instance.to_mongo().to_dict(), "update": True})
            form.fields[self.index_name].widget.attrs["readonly"] = True
            context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        try:
            form.create_update()
        except NotUniqueError:
            messages.error(self.request, f"{self.object_class.__name__} already exists in database.")
            return super().form_invalid(form)
        return super().form_valid(form)

# Create your views here.
class TreeInfoFormView(MyFormView):
    permission_required = 'TreeInfo.change_content'
    url_update_name = "treeinfo_update"
    url_create_name = "treeinfo_create"
    form_class = TreeInfoForm
    index_name = "name"
    object_class = TreeInfo


class BonsaiTechniqueFormView(MyFormView):
    permission_required = 'BonsaiAdvice.change_content'
    url_update_name = "technique_update"
    url_create_name = "technique_create"
    form_class = BonsaiTechniqueForm
    index_name = "short_name"
    object_class = BonsaiTechnique

class BonsaiObjectiveFormView(MyFormView):
    permission_required = 'BonsaiAdvice.change_content'
    url_update_name = "objective_update"
    url_create_name = "objective_create"
    form_class = BonsaiObjectiveForm
    index_name = "short_name"
    object_class = BonsaiObjective

class BonsaiWhenFormView(MyFormView):
    permission_required = 'BonsaiAdvice.change_content'
    url_update_name = "when_update"
    url_create_name = "when_create"
    form_class = BonsaiWhenForm
    index_name = "short_name"
    object_class = BonsaiWhen
