import { Component, OnDestroy } from '@angular/core';
import { NonNullableFormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import {
  BehaviorSubject,
  Observable,
  Subject,
  combineLatest,
  forkJoin,
  map,
  of,
  switchMap,
  take,
  takeUntil,
  tap,
} from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { TreeInfoService } from 'src/app/Services/tree-info.service';
import { periodIdToName } from 'src/app/utils';
import {
  BonsaiTechnique,
  PeriodEnum,
  TechniqueMapper,
  TreeInfo,
} from 'swagger-client';
import {
  InputType,
  SelectOption,
} from '../../Generic/text-input/custom-input.component';
@Component({
  selector: 'app-which-technique',
  templateUrl: './which-technique.component.html',
  styleUrls: ['./which-technique.component.scss'],
})
export class WhichTechniqueComponent implements OnDestroy {
  public InputType = InputType;
  public form = this.fb.group({
    tree: this.fb.control<string | undefined>(undefined, [Validators.required]),
    objective: this.fb.control<string | undefined>(undefined),
    period: this.fb.control<string | undefined>(undefined),
    stage: this.fb.control<string[]>([]),
  });

  public readonly treeOptions$: Observable<SelectOption[]> = this.treeService
    .getAllTreeInfo()
    .pipe(
      take(1),
      map((trees) =>
        trees.map(
          (tree): SelectOption => ({
            value: tree.name,
            label: tree.display_name,
          })
        )
      )
    );

  public readonly objectiveOptions$: Observable<SelectOption[]> =
    this.adviceService.getObjectives().pipe(
      take(1),
      map((objectives) =>
        objectives.map(
          (objective): SelectOption => ({
            value: objective.short_name,
            label: objective.display_name ?? '',
          })
        )
      )
    );

  public readonly stageOptions$: Observable<SelectOption[]> = this.adviceService
    .getStages()
    .pipe(
      take(1),
      map((stages) =>
        stages.map(
          (stage): SelectOption => ({
            value: stage.short_name,
            label: stage.display_name ?? '',
          })
        )
      )
    );

  public periodOptions: SelectOption[] = Object.keys(PeriodEnum).map((key) => {
    const stringKey = PeriodEnum[key as keyof typeof PeriodEnum];
    return {
      value: stringKey,
      label: periodIdToName(stringKey) ?? '',
    };
  });
  constructor(
    private fb: NonNullableFormBuilder,
    private adviceService: AdviceService,
    private treeService: TreeInfoService,
    private route: ActivatedRoute
  ) {
}
