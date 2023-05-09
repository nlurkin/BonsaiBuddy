from django.shortcuts import render
from .menu import BonsaiAdviceMenuMixin
from django.views import generic, View
from .models import BonsaiTechnique, BonsaiObjective, BonsaiWhen
from utils import get_object_or_404, user_has_any_perms
from django.urls import reverse_lazy
from .forms import AdviceConfigForm

class IndexView(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = "BonsaiAdvice/index.html"

    def get_queryset(self):
        # Not needed as this is done in the get_context_data, but required by django
        return None

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        show_unpublished = user_has_any_perms(self.request.user, ["BonsaiAdvice.change_content"])
        top["bonsai_techniques"] = BonsaiTechnique.get_all(not show_unpublished)
        top["bonsai_objectives"] = BonsaiObjective.get_all(not show_unpublished)
        top["bonsai_when"] = BonsaiWhen.get_all(not show_unpublished)
        return top

class TechniqueView(BonsaiAdviceMenuMixin, View):
    model = BonsaiTechnique
    template_name = "BonsaiAdvice/detail_technique.html"
    context_object_name = "technique"

    def get(self, request, pk):
        obj_instance = get_object_or_404(self.model, short_name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: obj_instance})

class ObjectiveView(BonsaiAdviceMenuMixin, View):
    model = BonsaiObjective
    template_name = "BonsaiAdvice/detail_objective.html"
    context_object_name = "objective"

    def get(self, request, pk):
        obj_instance = get_object_or_404(self.model, short_name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: obj_instance})


class WhenView(BonsaiAdviceMenuMixin, View):
    model = BonsaiWhen
    template_name = "BonsaiAdvice/detail_when.html"
    context_object_name = "when"

    def get(self, request, pk):
        obj_instance = get_object_or_404(self.model, short_name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: obj_instance})


class WhichTechniqueView(View):
    class ReqInfo():
        def __init__(self, query):
            self.tree = query.get("tree", None)
            self.objective = query.get("objective", None)
            self.period = query.get("period", None)
            self.when = query.get("when", None)

        def is_complete(self):
            # Requires tree, objective, and either of period or when
            return (not self.tree or not self.objective or not (self.period or self.when))

    template_name = "BonsaiAdvice/blank.html"
    def get(self, request):
        info = WhichTechniqueView.ReqInfo(request.GET)
        if info.is_complete():
            # Missing parameters
            return self.process_partial_request(info)
        else:
            return self.process_complete_request(info)

    def process_complete_request(self, info):
        '''To be used when all parameters are set correctly'''
        return render(self.request, self.template_name)

    def process_partial_request(self, info):
        '''To be used when some parameters are missing. Essentially telling user to complete and resubmit'''
        view = WhichTechniqueSelector.as_view(info=info)
        return view(self.request)

class WhichTechniqueSelector(BonsaiAdviceMenuMixin, generic.FormView):
    success_url = reverse_lazy("BonsaiAdvice:which_technique")
    template_name = 'BonsaiAdvice/advice_selector.html'
    form_class = AdviceConfigForm
    info = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get("is_submitted", False):
            # Forms has been submitted, bind it
            form = self.form_class({"tree": self.info.tree.lower(), "objective": self.info.objective, "period": self.info.period, "when": self.info.when, "is_submitted": True})
        else:
            form = self.form_class(initial={"tree": self.info.tree.lower(), "objective": self.info.objective, "period": self.info.period, "when": self.info.when})
        context['form'] = form
        return self.render_to_response(context)
