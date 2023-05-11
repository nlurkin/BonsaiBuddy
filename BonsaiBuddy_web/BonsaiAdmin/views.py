from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import TreeInfoForm, BonsaiTechniqueForm, BonsaiObjectiveForm, BonsaiWhenForm
from django.urls import reverse_lazy, reverse
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

    def init_form(self, pk):
        kwargs = {self.index_name: pk}
        obj_instance = get_object_or_404(self.object_class, **kwargs)
        form = self.form_class(initial={**obj_instance.to_mongo().to_dict(), "update": True})
        form.fields[self.index_name].widget.attrs["readonly"] = True
        return form

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "pk" in context:
            context['form'] = self.init_form(context["pk"])

        return self.render_to_response(context)

    def get_success_url(self):
        if "pk" in self.kwargs:
            return reverse(f"BonsaiAdmin:{self.url_update_name}", kwargs={"pk": self.kwargs["pk"]})
        return super().get_success_url()

    def process_form(self, form):
        try:
            form.create_update()
        except NotUniqueError:
            messages.error(self.request, f"{self.object_class.__name__} already exists in database.")
            return super().form_invalid(form)

    def form_valid(self, form):
        self.process_form(form)
        return super().form_valid(form)

# Create your views here.
class TreeInfoFormView(MyFormView):
    permission_required = 'TreeInfo.change_content'
    url_update_name = "treeinfo_update"
    url_create_name = "treeinfo_create"
    form_class = TreeInfoForm
    index_name = "name"
    object_class = TreeInfo

    def init_form_association(self, pk, data=None):
        if data is None:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True, extra=0)(initial=[{"tree_name": pk.lower(), "tree_name_hidden": pk.lower()}], prefix="association")
        else:
            form_association = forms.formset_factory(TechniqueAssociationForm, can_delete=True)(data, prefix="association")
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

    def form_valid(self, form):
        if isinstance(form, forms.BaseFormSet):
            return FormView.form_valid(self, form)
        else:
            return super().form_valid(form)


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
