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
import { filterDefined } from 'src/app/rxjs-util';
import { periodIdToName } from 'src/app/utils';
import {
  AssociationSearch,
  BonsaiTechnique,
  PeriodEnum,
  TechniqueMapper,
  TreeInfo,
} from 'swagger-client';
import {
  InputType,
  SelectOption,
} from '../../Generic/text-input/custom-input.component';

type MapperForDisplay = {
  technique: BonsaiTechnique | undefined;
  stages: string[];
  periods: string[];
  comment: string | undefined;
};

@Component({
  selector: 'app-which-technique',
  templateUrl: './which-technique.component.html',
  styleUrls: ['./which-technique.component.scss'],
})
export class WhichTechniqueComponent implements OnDestroy {
  public InputType = InputType;
  public form = this.fb.group({
    tree: this.fb.control<string | undefined>(undefined, [Validators.required]),
    objective: this.fb.control<string | undefined>(undefined, [
      Validators.required,
    ]),
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

  private initialOptions$: Observable<{
    oid: string | null;
    tree: string | null;
  }> = this.route.queryParamMap.pipe(
    map((params) => {
      const tree = params.get('tree');
      const oid = params.get('oid');
      return { oid, tree };
    })
  );

  private readonly initialSelectedTree$: Observable<TreeInfo | undefined> =
    this.initialOptions$.pipe(
      switchMap(({ tree }) =>
        tree ? this.treeService.getTreeInfo(tree) : of(undefined)
      )
    );
  private readonly selectedSearchTreeName$: BehaviorSubject<
    string | undefined
  > = new BehaviorSubject<string | undefined>(undefined);
  private readonly selectedSearchTree$: Observable<TreeInfo | undefined> =
    this.selectedSearchTreeName$.pipe(
      filterDefined(),
      switchMap((name) => this.treeService.getTreeInfo(name))
    );
  private readonly mapperByOid$: Observable<TechniqueMapper | undefined> =
    combineLatest([
      this.initialOptions$.pipe(map(({ oid }) => oid)),
      this.initialSelectedTree$,
    ]).pipe(
      map(([oid, tree]) => tree?.techniques.find((t) => t.oid === oid)),
      tap((maybeMapper) => {
        if (maybeMapper) this.showSearch$.next(false);
      })
    );
  private readonly mapperBySearch$: BehaviorSubject<
    TechniqueMapper[] | undefined
  > = new BehaviorSubject<TechniqueMapper[] | undefined>(undefined);

  public readonly selectedTree$: Observable<TreeInfo> = combineLatest([
    this.initialSelectedTree$,
    this.selectedSearchTree$,
  ]).pipe(
    map(([initial, search]) => (search ? search : initial)),
    filterDefined()
  );

  public readonly mapperSelector$: Observable<MapperForDisplay[]> =
    combineLatest([this.mapperByOid$, this.mapperBySearch$]).pipe(
      map(([byOid, bySearch]) =>
        bySearch ? bySearch : byOid ? [byOid] : undefined
      ),
      filterDefined(),
      switchMap((mappers) =>
        forkJoin(
          mappers.map((mapper) => {
            const adviceRequest = this.adviceService
              .getTechniqueById(mapper.technique.id)
              .pipe(take(1));
            const periodRequest =
              mapper.stage.length > 0
                ? forkJoin(
                    mapper.stage.map((stage) =>
                      this.adviceService.getStageById(stage.id).pipe(take(1))
                    )
                  )
                : of([]);
            return combineLatest([adviceRequest, periodRequest]).pipe(
              map(([technique, stages]) => ({
                technique,
                stages,
                periods: mapper.period.map((period) => periodIdToName(period)),
                comment: mapper.comment,
              }))
            );
          })
        )
      ),
      map((mappers) => {
        return mappers.map(
          ({ technique, stages, periods, comment }): MapperForDisplay => {
            return {
              technique,
              stages: stages
                .map((stage) => stage?.display_name)
                .filter((stage): stage is string => !!stage),
              periods: periods.filter((period): period is string => !!period),
              comment,
            };
          }
        );
      })
    );

  public readonly showSearch$ = new BehaviorSubject<boolean>(true);

  private destroy$ = new Subject<void>();

  constructor(
    private fb: NonNullableFormBuilder,
    private adviceService: AdviceService,
    private treeService: TreeInfoService,
    private route: ActivatedRoute
  ) {
    this.initialOptions$
      .pipe(takeUntil(this.destroy$))
      .subscribe(({ tree }) => {
        if (tree) this.form.patchValue({ tree: tree });
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  public submitSearch() {
    if (this.form.invalid) return;

    const formValues = this.form.getRawValue();
    const request: AssociationSearch = {
      tree: formValues.tree!,
      objective: formValues.objective!,
      period: formValues.period,
      stage: formValues.stage ?? [],
    };

    this.adviceService
      .searchAssociations(request)
      .pipe(take(1))
      .subscribe((mappers) => {
        this.selectedSearchTreeName$.next(formValues.tree);
        this.mapperBySearch$.next(mappers.techniques);
        this.showSearch$.next(false);
      });
  }
}
