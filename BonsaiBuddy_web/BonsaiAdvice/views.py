from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from BonsaiAdvice.serializers import (BonsaiObjectiveSerializer,
                                      BonsaiTechniqueSerializer)
from BonsaiBuddy.serializers import StringListSerializer
from TreeInfo.models import TreeInfo
from utils import get_object_or_404, user_has_any_perms

from .forms import AdviceConfigForm, ReqAdviceInfo
from .menu import BonsaiAdviceMenuMixin
from .models import (AdvicePermissionModelAPI, BonsaiObjective, BonsaiStage,
                     BonsaiTechnique, get_technique_categories, make_timing,
                     timing_matches)


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
        top["bonsai_stage"] = BonsaiStage.get_all(not show_unpublished).order_by("sequence")
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


class StageView(BonsaiAdviceMenuMixin, View):
    model = BonsaiStage
    template_name = "BonsaiAdvice/detail_stage.html"
    context_object_name = "stage"

    def get(self, request, pk):
        obj_instance = get_object_or_404(self.model, short_name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: obj_instance})


class WhichTechniqueView(View):
    def get(self, request):
        info = ReqAdviceInfo(request.GET)
        if not info.is_complete():
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
            form = self.form_class({"tree": self.info.tree, "objective": self.info.objective, "period": self.info.period, "stage": self.info.stage, "is_submitted": True})
        else:
            form = self.form_class(initial={"tree": self.info.tree, "objective": self.info.objective, "period": self.info.period, "stage": self.info.stage})
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

        tree = self.get_queryset()

        if self.info.oid is not None:
            use_oid = True
        else:
            # Then get the list of valid advices according to the criteria in info
            objective_document_id = BonsaiObjective.get(self.info.objective).id
            stage_document_id = None if not self.info.stage else [BonsaiStage.get(_).id for _ in self.info.stage]
            period = None if not self.info.period else self.info.period.split(',')

        selected_techniques = []
        for technique in tree.techniques:
            if use_oid:
                if str(technique.oid) != self.info.oid:
                    continue
            else:
                if technique.objective.id != objective_document_id:
                    continue
                if not timing_matches(stage_document_id, period, [_.id for _ in technique.stage], technique.period):
                    continue
            technique_doc = technique.technique.fetch()
            if not show_unpublished and not technique_doc.published:
                continue
            selected_techniques.append({"technique": technique_doc,
                                        "timing": make_timing([_.fetch() for _ in technique.stage], technique.period),
                                        "comment": technique.comment})
        context["techniques"] = selected_techniques
        context["tree"] = tree
        return context


@extend_schema_view(retrieve=extend_schema(parameters=[OpenApiParameter("short_name", str, OpenApiParameter.PATH)]))
class BonsaiTechniqueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BonsaiTechnique to be viewed or edited.
    """
    lookup_field = 'short_name'
    serializer_class = BonsaiTechniqueSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, AdvicePermissionModelAPI]

    def get_queryset(self):
        """
        This view should return a list of all the published 
        techniques unless the user has permissions.
        """
        show_unpublished = user_has_any_perms(
            self.request.user, ["BonsaiAdvice.change_content"])
        return BonsaiTechnique.get_all(
            not show_unpublished).order_by("sequence")


@extend_schema_view(retrieve=extend_schema(parameters=[OpenApiParameter("short_name", str, OpenApiParameter.PATH)]))
class BonsaiObjectiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BonsaiObjective to be viewed or edited.
    """
    lookup_field = 'short_name'
    serializer_class = BonsaiObjectiveSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, AdvicePermissionModelAPI]

    def get_queryset(self):
        """
        This view should return a list of all the published
        objectives unless the user has permissions.
        """
        show_unpublished = user_has_any_perms(
            self.request.user, ["BonsaiAdvice.change_content"])
        return BonsaiObjective.get_all(
            not show_unpublished).order_by("sequence")


class BonsaiTechniqueCategoriesView(GenericAPIView):
    """
    API endpoint that returns the list of technique categories
    """
    serializer_class = StringListSerializer

    def get(self, request, format=None):
        serializer = self.get_serializer(
            get_technique_categories(), many=True)
        return Response(serializer.data)
