# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import TreeInfo
from django.views import View, generic
from utils import get_object_or_404, user_has_any_perms
from .menu import TreeInfoMenuMixin
from BonsaiAdvice.models import periodid_to_name

class IndexView(TreeInfoMenuMixin, generic.ListView):
    template_name = "TreeInfo/index.html"
    context_object_name = "tree_info_list"

    def get_queryset(self):
        """Return the complete list of available trees."""
        show_unpublished = user_has_any_perms(self.request.user, ["TreeInfo.change_content"])
        treeinfo = TreeInfo.objects
        if not show_unpublished:
            treeinfo = treeinfo.filter(published=True)
        return treeinfo.order_by("name")

class DetailView(TreeInfoMenuMixin, View):
    model = TreeInfo
    template_name = "TreeInfo/detail.html"
    context_object_name = "tree_info"

    def get(self, request, pk):
        tree = get_object_or_404(self.model, name=pk)
        return render(request, self.template_name, {**self.build_menu_context(request), self.context_object_name: tree,
                                                    "technique_table": self.build_technique_table(tree)})

    def build_technique_table(self, tree):
        show_unpublished = user_has_any_perms(self.request.user, ["TreeInfo.change_content"])

        # Fetch all associations for the tree
        tech_associations = tree.techniques
        if len(tech_associations) == 0:
            return []
        for association in tech_associations:
            association.fetch()

        # Take all distinct objectives and sort them according to sequence
        # Consider that several may share the same sequence, so use the name
        # also in the index
        all_objectives = {(_.objective_f.sequence, _.objective_f.short_name): _.objective_f.display_name for _ in tech_associations}
        all_objectives_ordered = [all_objectives[_] for _ in sorted(all_objectives)]

        # Prepare the table (header row)
        table = [[""] + all_objectives_ordered]

        technique_seen = []
        techniques_by_category = {_.technique_f.category: [] for _ in tech_associations}
        for association in tech_associations:
            # Do not repeat techniques appearing multiple times
            if association.technique in technique_seen:
                continue
            technique_seen.append(association.technique)
            if not show_unpublished and not association.technique_f.published:
                continue

            # Search for all associations sharing the same technique
            similar = [_ for _ in tech_associations if _.technique == association.technique]

            # Categorize them according to their objective
            objectives = {_: [] for _ in all_objectives_ordered}
            for technique in similar:
                stage = ",".join(technique.stage_f)
                periods = ", ".join([periodid_to_name(_) for _ in technique.period])
                timing = periods
                if len(stage)>0:
                    timing += f" ({stage})"
                # But for each save only the timing and the link to the full description
                objectives[technique.objective_f.display_name].append(timing + " " + technique.link(tree.name))
            # Add the technique as a row in the table
            techniques_by_category[association.technique_f.category].append([association.technique_f.link()] + ["\n".join(objectives[_]) for _ in all_objectives_ordered])

        for category in techniques_by_category:
            table.append([category.capitalize()])
            table.extend(techniques_by_category[category])

        return table