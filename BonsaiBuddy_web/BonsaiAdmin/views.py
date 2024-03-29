from BonsaiAdvice.models import BonsaiObjective, BonsaiTechnique, BonsaiStage
from BonsaiBuddy.views import CreateUpdateView
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView
from TreeInfo.models import TreeInfo
from utils import user_has_any_perms

from .forms import (BonsaiObjectiveForm, BonsaiTechniqueForm, BonsaiStageForm,
                    TechniqueAssociationForm, TreeInfoForm)
from .menu import AdminMenuMixin
from copy import deepcopy



class IndexView(AdminMenuMixin, PermissionRequiredMixin, View):
    permission_required = ['TreeInfo.change_content',
                           "BonsaiAdvice.change_content"]

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
    display_url = "TreeInfo:detail"
    page_title = "Tree info"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.copy_tree = None

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        if self.copy_tree:
            form = self.form_class(initial={**self.obj_to_dict(self.copy_tree), "update": False})
            form.fields[self.index_name].widget.attrs["readonly"] = True
            top["form"] = form
        return top

    def init_form_association(self, pk, data=None):
        initial = [{"tree_name": pk.lower(), "tree_name_hidden": pk,
                    "display_name": technique["technique_name"] if "technique_name" in technique else "", **technique}
                   for technique in TreeInfo.get(pk).get_techniques_list(sort=self.request.GET.get("sort", None))]
        if data is None:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True, extra=0)(
                initial=initial, prefix="association")
        else:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True)(
                data, initial=initial, prefix="association")
        return form_association

    def get(self, request, *args, **kwargs):
        clone_tree = request.GET.get("tree", None)
        if clone_tree:
            self.copy_tree = deepcopy(TreeInfo.get(clone_tree))#
            self.copy_tree.id = None
            self.copy_tree.name = None
            self.copy_tree.display_name = None
            self.copy_tree.latin_name = None
        form_association = self.init_form_association(
            kwargs["pk"]) if "pk" in kwargs else None
        return super().get(request, form_association=form_association, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.POST.get("association-TOTAL_FORMS", None):
            # Dealing with default form, forward to parent
            form_association = self.init_form_association(
                kwargs["pk"]) if "pk" in kwargs else None
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
    display_url = "BonsaiAdvice:technique_detail"
    page_title = "Bonsai Technique"


class BonsaiObjectiveFormView(MyFormView):
    permission_required = 'BonsaiAdvice.change_content'
    url_update_name = "objective_update"
    url_create_name = "objective_create"
    form_class = BonsaiObjectiveForm
    index_name = "short_name"
    object_class = BonsaiObjective
    display_url = "BonsaiAdvice:objective_detail"
    page_title = "Bonsai Objective"


class BonsaiStageFormView(MyFormView):
    permission_required = 'BonsaiAdvice.change_content'
    url_update_name = "stage_update"
    url_create_name = "stage_create"
    form_class = BonsaiStageForm
    index_name = "short_name"
    object_class = BonsaiStage
    display_url = "BonsaiAdvice:stage_detail"
    page_title = "Bonsai Stage"
