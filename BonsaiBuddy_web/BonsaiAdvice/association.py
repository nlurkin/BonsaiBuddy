

from BonsaiAdvice.forms import ReqAdviceInfo
from BonsaiAdvice.models import BonsaiObjective, BonsaiStage, make_timing, timing_matches
import TreeInfo


def select_associations(tree: TreeInfo, query_info: ReqAdviceInfo, show_unpublished: bool, for_api: bool = False):
    if query_info.oid is not None:
        use_oid = True
    else:
        # Then get the list of valid advices according to the criteria in info
        objective_document_id = BonsaiObjective.get(query_info.objective).id
        stage_document_id = None if not query_info.stage else [
            BonsaiStage.get(_).id for _ in query_info.stage]
        period = None if not query_info.period else query_info.period.split(
            ',')
        use_oid = False

    selected_techniques = []
    for technique in tree.techniques:
        if use_oid:
            if str(technique.oid) != query_info.oid:
                continue
        else:
            if technique.objective.id != objective_document_id:
                continue
            if not timing_matches(stage_document_id, period, [_.id for _ in technique.stage], technique.period):
                continue
        technique_doc = technique.technique.fetch()
        if not show_unpublished and not technique_doc.published:
            continue
        if for_api:
            selected_techniques.append(technique)
        else:
            selected_techniques.append({"technique": technique_doc,
                                        "timing": make_timing([_.fetch() for _ in technique.stage], technique.period),
                                        "comment": technique.comment})

        return selected_techniques
