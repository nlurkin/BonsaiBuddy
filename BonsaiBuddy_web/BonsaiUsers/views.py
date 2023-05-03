from django.shortcuts import render
from .menu import BonsaiUsersMenuMixin
from django.views import View, generic
from .models import UserProfile
from utils import get_object_or_404
from django.http import Http404
from .forms import CustomUserCreationForm, UpdateUserProfileForm, ModifyPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth import views

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

class MyLoginView(BonsaiUsersMenuMixin, views.LoginView):
    pass

class ProfileUpdateView(BonsaiUsersMenuMixin, generic.FormView):
    success_url = reverse_lazy("Profile:detail")
    template_name = 'BonsaiUsers/profile_form.html'
    form_class = UpdateUserProfileForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        user = UserProfile.get_user(request.user.username)
        form = self.form_class(initial={**user.to_mongo().to_dict(), "update": True})
        context['form'] = form

        return self.render_to_response(context)

    def form_valid(self, form):
        form.save(self.request.user.username)
        return super().form_valid(form)

class ModifyPasswordView(BonsaiUsersMenuMixin, generic.FormView):
    form_class = ModifyPasswordForm
    success_url = reverse_lazy("Profile:detail")
    template_name = "registration/password_change.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save(self.request.user.username)
        return super().form_valid(form)