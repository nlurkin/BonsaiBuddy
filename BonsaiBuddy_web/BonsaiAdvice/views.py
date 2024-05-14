from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_mongoengine import viewsets

from BonsaiAdvice.association import select_associations
from BonsaiAdvice.serializers import (AssociationSearchResultSerializer,
                                      AssociationSearchSerializer,
                                      BonsaiObjectiveSerializer,
                                      BonsaiStageSerializer,
                                      BonsaiTechniqueSerializer)
from BonsaiBuddy.serializers import StringListSerializer
from TreeInfo.models import TreeInfo
from utils import get_object_or_404, user_has_any_perms

from .forms import AdviceConfigForm, ReqAdviceInfo
from .menu import BonsaiAdviceMenuMixin
from .models import (AdvicePermissionModelAPI, BonsaiObjective, BonsaiStage,
                     BonsaiTechnique, get_technique_categories)


class IndexView(BonsaiAdviceMenuMixin, generic.ListView):
    template_name = "BonsaiAdvice/index.html"

    def get_queryset(self):
        # Not needed as this is done in the get_context_data, but required by django
        return None

    def get_context_data(self, **kwargs):
        top = super().get_context_data(**kwargs)
        show_unpublished = user_has_any_perms(
            self.request.user, ["BonsaiAdvice.change_content"])
        technique_list = []
        for category in get_technique_categories():
            technique_list.append((category, BonsaiTechnique.get_all(
                not show_unpublished, category=category.lower()).order_by("sequence")))

        top["bonsai_techniques"] = technique_list
        top["bonsai_objectives"] = BonsaiObjective.get_all(
            not show_unpublished).order_by("sequence")
        top["bonsai_stage"] = BonsaiStage.get_all(
            not show_unpublished).order_by("sequence")
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
            form = self.form_class({"tree": self.info.tree, "objective": self.info.objective,
                                   "period": self.info.period, "stage": self.info.stage, "is_submitted": True})
        else:
            form = self.form_class(initial={
                                   "tree": self.info.tree, "objective": self.info.objective, "period": self.info.period, "stage": self.info.stage})
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
        show_unpublished = user_has_any_perms(
            self.request.user, ["BonsaiAdvice.change_content"])

        tree = self.get_queryset()

        selected_techniques = select_associations(
            tree, self.info, show_unpublished)

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


@extend_schema_view(retrieve=extend_schema(parameters=[OpenApiParameter("short_name", str, OpenApiParameter.PATH)]))
class BonsaiStageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BonsaiStage to be viewed or edited.
    """
    lookup_field = 'short_name'
    serializer_class = BonsaiStageSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, AdvicePermissionModelAPI]

    def get_queryset(self):
        """
        This view should return a list of all the published
        stages unless the user has permissions.
        """
        show_unpublished = user_has_any_perms(
            self.request.user, ["BonsaiAdvice.change_content"])
        return BonsaiStage.get_all(
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


class AssociationSearchView(APIView):
    """
    API endpoint that returns the list of technique categories
    """
    authentication_classes = []
    permission_classes = []

    @extend_schema(operation_id="adviceAssociationSearch", request=AssociationSearchSerializer, responses={200: AssociationSearchResultSerializer})
    def post(self, request, *args, **kwargs):
        input_serializer = AssociationSearchSerializer(data=request.data)
        if input_serializer.is_valid():
            # Process the data and create your output data
            request_data = input_serializer.validated_data
            tree = TreeInfo.get(request_data["tree"])
            show_unpublished = user_has_any_perms(
                self.request.user, ["BonsaiAdvice.change_content"])
            output_data = select_associations(tree, ReqAdviceInfo(None,
                                                                  serialized_data=request_data), show_unpublished, for_api=True)
            output_serializer = AssociationSearchResultSerializer(
                {'techniques': output_data})
            return Response(output_serializer.data, status=200)
        else:
            return Response(input_serializer.errors, status=400)
