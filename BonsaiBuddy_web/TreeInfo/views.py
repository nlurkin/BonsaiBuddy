# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Question, Choice, TreeInfo
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from utils import get_object_or_404

class IndexView(generic.ListView):
    template_name = "TreeInfo/index.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        return TreeInfo.objects.filter(published=True).order_by("name")

class DetailView(View):
    model = TreeInfo
    template_name = "TreeInfo/detail.html"
    context_object_name = "tree_info"

    def get(self, request, pk):
        question = get_object_or_404(self.model, name=pk)
        return render(request, self.template_name, {self.context_object_name: question})

class ResultsView(DetailView):
    template_name = "TreeInfo/results.html"

from django.views.generic.edit import FormView
from .forms import CreateForm
from django.contrib.auth.mixins import UserPassesTestMixin

class CreateFormView(UserPassesTestMixin, FormView):
    template_name = 'TreeInfo/create.html'
    form_class = CreateForm
    success_url = reverse_lazy("TreeInfo:index")

    def test_func(self):
        return self.request.user.has_perm('TreeInfo.change_content')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create()
        return super().form_valid(form)

class VoteView(View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        try:
            selected_choice = question.choices.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(
                request,
                "TreeInfo/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("TreeInfo:results", args=(question.id,)))