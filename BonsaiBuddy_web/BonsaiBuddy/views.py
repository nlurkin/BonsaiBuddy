from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from mongoengine.errors import NotUniqueError
from utils import get_object_or_404


class CreateUpdateView(FormView):
    # Required in subclass: success_url, template_name, app_name

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        if "pk" in top:
            top["rev_url"] = f"{self.app_name}:{self.url_update_name}"
        else:
            top["rev_url"] = f"{self.app_name}:{self.url_create_name}"
        return top

    def init_form(self, pk):
        kwargs = {self.index_name: pk}
        obj_instance = get_object_or_404(self.object_class, **kwargs)
        form = self.form_class(
            initial={**obj_instance.to_mongo().to_dict(), "update": True})
        form.fields[self.index_name].widget.attrs["readonly"] = True
        return form

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "pk" in context:
            context['form'] = self.init_form(context["pk"])

        return self.render_to_response(context)

    def get_success_url(self):
        if "pk" in self.kwargs:
            return reverse(f"{self.app_name}:{self.url_update_name}", kwargs={"pk": self.kwargs["pk"]})
        return super().get_success_url()

    def process_form(self, form, **kwargs):
        try:
            form.create_update(**kwargs)
        except NotUniqueError:
            messages.error(
                self.request, f"{self.object_class.__name__} already exists in database.")
            return super().form_invalid(form)

    def form_valid(self, form):
        self.process_form(form)
        return super().form_valid(form)
