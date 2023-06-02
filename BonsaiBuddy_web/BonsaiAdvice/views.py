from django.shortcuts import render
from .menu import BonsaiAdviceMenuMixin
from django.views import generic, View
from .models import BonsaiTechnique, BonsaiObjective, BonsaiWhen, timing_matches, make_timing, get_technique_categories
from utils import get_object_or_404, user_has_any_perms
from django.urls import reverse_lazy
from .forms import AdviceConfigForm, ReqAdviceInfo
from TreeInfo.models import TreeInfo

class IndexView(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = "BonsaiAdvice/index.html"

    def get_queryset(self):
        # Not needed as this is done in the get_context_data, but required by django
        return None

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        show_unpublished = user_has_any_perms(self.request.user, ["BonsaiAdvice.change_content"])
        technique_list = []
        for category in get_technique_categories():
            technique_list.append((category, BonsaiTechnique.get_all(not show_unpublished, category=category.lower()).order_by("sequence")))

        top["bonsai_techniques"] = technique_list
        top["bonsai_objectives"] = BonsaiObjective.get_all(not show_unpublished).order_by("sequence")
        top["bonsai_when"] = BonsaiWhen.get_all(not show_unpublished).order_by("sequence")
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
    def get(self, request):
        info = ReqAdviceInfo(request.GET)
        if info.is_complete():
            # Missing parameters
            return self.process_partial_request(info)
        else:
            return self.process_complete_request(info)

    def process_complete_request(self, info):
        '''To be used when all parameters are set correctly'''
        view = WhichTechniqueDisplay.as_view(info=info)
        return view(self.request)

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
            form = self.form_class({"tree": self.info.tree, "objective": self.info.objective, "period": self.info.period, "when": self.info.when, "is_submitted": True})
        else:
            form = self.form_class(initial={"tree": self.info.tree, "objective": self.info.objective, "period": self.info.period, "when": self.info.when})
        context['form'] = form
        return self.render_to_response(context)


class WhichTechniqueDisplay(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = 'BonsaiAdvice/advice_display.html'
    context_object_name = "techniques"
    info = None

    def get_queryset(self):
        return TreeInfo.get(self.info.tree)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_unpublished = user_has_any_perms(self.request.user, ["BonsaiAdvice.change_content"])

        # Then get the list of valid advices according to the criteria in info
        objective_document_id = BonsaiObjective.get(self.info.objective).id
        when_document_id = None if not self.info.when else [BonsaiWhen.get(_).id for _ in self.info.when]
        period = None if not self.info.period else self.info.period.split(',')
        selected_techniques = []
        tree = self.get_queryset()
        for technique in tree.techniques:
            if technique.objective.id != objective_document_id:
                continue
            if not timing_matches(when_document_id, period, [_.id for _ in technique.when], technique.period):
                continue
            technique_doc = technique.technique.fetch()
            if not show_unpublished and not technique_doc.published:
                continue
            selected_techniques.append({"technique": technique_doc,
                                        "timing": make_timing([_.fetch() for _ in technique.when], technique.period)})
        context["techniques"] = selected_techniques
        context["tree"] = tree
        return context