from django.shortcuts import render
from .menu import BonsaiUsersMenuMixin
from django.views import View, generic
from .models import UserProfile, TreeCollection
from utils import get_object_or_404
from django.http import Http404
from .forms import CustomUserCreationForm, UpdateUserProfileForm, ModifyPasswordForm, MyTreeForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth import views
from BonsaiBuddy.views import CreateUpdateView
from bson import ObjectId


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
        up = form.save()
        user = authenticate(self.request, username=up.username, password=up.password)
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

class MyTreesListView(BonsaiUsersMenuMixin, generic.ListView):
    template_name = "BonsaiUsers/my_trees_list.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        profile = UserProfile.get_user(self.request.user.username)
        trees_list = profile.my_trees
        return trees_list

class MyTreesFormView(BonsaiUsersMenuMixin, CreateUpdateView):
    template_name = "BonsaiUsers/my_trees_form.html"
    url_update_name = "my_trees_update"
    url_create_name = "my_trees_create"
    app_name = "Profile"
    form_class = MyTreeForm
    index_name = "oid"
    object_class = TreeCollection
    success_url  = reverse_lazy("Profile:my_trees")

    def form_valid(self, form):
        self.process_form(form, username=self.request.user.username)
        return generic.FormView.form_valid(self, form)

    def get_object(self, pk, **kwargs):
        profile = UserProfile.get_user(self.request.user.username)
        tree = profile.get_my_tree(pk)
        if tree is not None:
            return tree

        raise Http404(f"TreeCollection {tree.oid} does not exist for user {self.request.user.username}")

    def obj_to_dict(self, obj):
        return {"oid": obj.oid, "tree_name": obj.treeReference.name, "objective": obj.objective.short_name}