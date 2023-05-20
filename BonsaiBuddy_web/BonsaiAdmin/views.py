from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TreeInfoForm, BonsaiTechniqueForm, BonsaiObjectiveForm, BonsaiWhenForm, TechniqueAssociationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from mongoengine.errors import NotUniqueError
from django.contrib import messages
from .menu import AdminMenuMixin
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen
from utils import get_object_or_404, user_has_any_perms
from django import forms

from BonsaiBuddy.views import CreateUpdateView
class IndexView(AdminMenuMixin, PermissionRequiredMixin, View):
    permission_required = ['TreeInfo.change_content', "BonsaiAdvice.change_content"]

    def has_permission(self):
        return user_has_any_perms(self.request.user, self.permission_required)

    def get(self, request):
        return render(request, "BonsaiAdmin/index.html", self.build_menu_context(request))


class MyFormView(AdminMenuMixin, PermissionRequiredMixin, CreateUpdateView):
    success_url = reverse_lazy("BonsaiAdmin:index")
    template_name = 'BonsaiAdmin/object_admin_form.html'
    app_name = "BonsaiAdmin"



class TreeInfoFormView(MyFormView):
    permission_required = 'TreeInfo.change_content'
    url_update_name = "treeinfo_update"
    url_create_name = "treeinfo_create"
    form_class = TreeInfoForm
    index_name = "name"
    object_class = TreeInfo

    def init_form_association(self, pk, data=None):
        initial=[{"tree_name": pk.lower(), "tree_name_hidden": pk, **technique} for technique in TreeInfo.get(pk).get_techniques_list()]
        if data is None:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True, extra=0)(
                initial=initial, prefix="association")
        else:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True)(
                data, initial=initial, prefix="association")
        return form_association

    def get(self, request, *args, **kwargs):
        form_association = self.init_form_association(kwargs["pk"]) if "pk" in kwargs else None
        return super().get(request, form_association=form_association, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.POST.get("association-TOTAL_FORMS", None):
            # Dealing with default form, forward to parent
            print("Using parent POST")
            form_association = self.init_form_association(kwargs["pk"]) if "pk" in kwargs else None
            return super().post(request, form_association=form_association, *args, **kwargs)

        # Dealing with the special form_association
        pk = kwargs["pk"]
        formset = self.init_form_association(pk, request.POST)

        if not formset.is_valid():
            return self.form_invalid(formset, pk)
        return self.form_valid(formset)

    def form_valid(self, formset):
        if isinstance(formset, forms.BaseFormSet):
            for form in formset:
                form.create_update()
            return FormView.form_valid(self, formset)
        else:
            return super().form_valid(formset)


    def form_invalid(self, form, pk):
        return self.render_to_response(self.get_context_data(form_association=form, pk=pk, form=self.init_form(pk)))


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
