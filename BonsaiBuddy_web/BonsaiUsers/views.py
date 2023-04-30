from django.shortcuts import render
from .menu import BonsaiUsersMenuMixin
from django.views import View, generic
from .models import UserProfile
from utils import get_object_or_404
from django.http import Http404
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

class DetailView(BonsaiUsersMenuMixin, View):
    model = UserProfile
    template_name = "BonsaiUsers/profile.html"
    context_object_name = "profile"

    def get(self, request):
        try:
            profile = get_object_or_404(self.model, username=request.user.username)
        except Http404:
            return render(request, "BonsaiUsers/not_found.html", {**self.build_menu_context(request), self.context_object_name: request.user})
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: profile})

class SignupView(BonsaiUsersMenuMixin, generic.FormView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("Profile:detail")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        username, password = form.save()
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)