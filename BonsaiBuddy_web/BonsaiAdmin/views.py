from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import CreateForm
from django.urls import reverse_lazy
from django.views.generic import View
class IndexView(View):
    def get(self, request):
        return render(request, "BonsaiAdmin/index.html")

# Create your views here.
class CreateTreeInfoFormView(UserPassesTestMixin, FormView):
    template_name = 'BonsaiAdmin/create_treeinfo.html'
    form_class = CreateForm
    success_url = reverse_lazy("BonsaiAdmin:index")

    def test_func(self):
        return self.request.user.has_perm('TreeInfo.change_content')

    def form_valid(self, form):
        form.create()
        return super().form_valid(form)