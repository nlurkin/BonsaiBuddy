import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as _ from 'lodash';
import {
  Observable,
  combineLatest,
  map,
  shareReplay,
  switchMap,
  take,
} from 'rxjs';
import { AdviceService, BonsaiEntity } from 'src/app/Services/advice.service';
import { TreeInfoService } from 'src/app/Services/tree-info.service';
import { UserService } from 'src/app/Services/user.service';
import { filterNullish } from 'src/app/rxjs-util';
import { periodToMonth, standardEntitySort } from 'src/app/utils';
import {
  BonsaiObjective,
  BonsaiStage,
  BonsaiTechnique,
  LazyReferenceField,
  TechniqueMapper,
} from 'swagger-client';
import { PeriodEvent } from '../../Advices/timeline/timeline.component';

@Component({
  selector: 'app-tree-detail',
  templateUrl: './tree-detail.component.html',
  styleUrls: ['./tree-detail.component.scss'],
})
export class TreeDetailComponent {
  public canEdit$: Observable<boolean> =
    this.userService.currentUserHasPermissions('BonsaiAdvice.change_content');

  public readonly tree$ = this.route.paramMap.pipe(
    map((params) => params.get('id')),
    filterNullish(),
    switchMap((id) => this.treeService.getTreeInfo(id)),
    take(1),
    shareReplay({ bufferSize: 1, refCount: true })
  );
  private techniqueMappers$ = this.tree$.pipe(map((tree) => tree.techniques));

  public readonly stageForTree$ = this.extractEntityForTree<BonsaiStage>(
    this.adviceService.getStages(),
    (techniqueMapper: TechniqueMapper) => techniqueMapper.stage
  );
  public readonly sortedObjectives$ = this.adviceService
    .getObjectives()
    .pipe(map((objectivesMap) => [...objectivesMap].sort(standardEntitySort)));

  private techniquesForTree$ = this.extractEntityForTree<BonsaiTechnique>(
    this.adviceService.getTechniques(),
    (techniqueMapper: TechniqueMapper) => [techniqueMapper.technique]
  );

  public techniqueMapperGeoupedByTechniqueAndObjective$ = combineLatest([
    this.techniqueMappers$,
    this.techniquesForTree$,
    this.sortedObjectives$,
  ]).pipe(
    map(([techniqueMappers, techniqueMap, sortedObjectives]) => {
      // The following does a three-level grouping of the techniqueMappers
      // - First by technique category
      // - Second by technique
      // - Last by objective
      // Each level consist in a list of objects sorted according to some rules:
      //  - By sequence id then lexically (for groups with sequence id) or just lexically
      // The object in each item of the lists contains the id/name of the group, the complete object
      // representing the group (i.e. the BonsaiTechnique or BonsaiObjective), and the nested
      // list group (values).
      const mapByCategory = _(techniqueMappers)
        .groupBy(
          (mapper) => techniqueMap.get(mapper.technique.id)?.category ?? ''
        )
        .map((mapper, category) => {
          const mapByTechnique = _(mapper)
            .groupBy((mapper) => mapper.technique.id)
            .map((mapper, techniqueId) => {
              const mapByObjective = sortedObjectives.reduce(
                (acc, objective) => ({
                  ...acc,
                  [objective.display_name ?? 'not_known']: mapper.filter(
                    (mapper) => mapper.objective.id === objective.id
                  ),
                }),
                {} as Record<string, TechniqueMapper[]>
              );

              return {
                techniqueId,
                technique: techniqueMap.get(techniqueId),
                values: mapByObjective,
              };
            })
            // .filter((mapper) => !!mapper.technique)
            .sort((a, b) => standardEntitySort(a.technique, b.technique))
            .value();
          return { category, values: mapByTechnique };
        })
        .sortBy((category) => category.category)
        .value();
      return mapByCategory;
    })
  );
  public colourLessEvents$!: Observable<PeriodEvent[]>;

  constructor(
    private route: ActivatedRoute,
    private treeService: TreeInfoService,
    private adviceService: AdviceService,
    private userService: UserService
  ) {}

  private extractEntityForTree<T extends BonsaiEntity>(
    entityList$: Observable<T[]>,
    entityExtractor: (entity: TechniqueMapper) => LazyReferenceField[]
  ) {
    return combineLatest([this.techniqueMappers$, entityList$]).pipe(
      map(([techniqueMapper, allEntities]): [string, T][] => {
        const treeEntityIds = techniqueMapper.flatMap((techniqueMapper) =>
          entityExtractor(techniqueMapper).map((entity) => entity.id)
        );
        return allEntities
          .filter((entity) => treeEntityIds.includes(entity.id))
          .map((entity): [string, T] => [entity.id, entity]);
      }),
      map((techniques) => new Map<string, T>(techniques))
    );
  }

  ngOnInit() {
    this.colourLessEvents$ = this.techniqueMappers$.pipe(
      switchMap((techniqueMappers) => {
        const val = techniqueMappers.map((techniqueMap) =>
          combineLatest([
            this.adviceService.getTechniqueById(techniqueMap.technique.id),
            this.adviceService.getObjectiveById(techniqueMap.objective.id),
          ]).pipe(
            map(([technique, objective]) => ({
              technique,
              objective,
              mapper: techniqueMap,
            }))
          )
        );
        return combineLatest(val);
      }),
      map((techniques) =>
        techniques.filter(
          (
            technique
          ): technique is {
            technique: BonsaiTechnique;
            objective: BonsaiObjective;
            mapper: TechniqueMapper;
          } => !!technique && !!technique.technique && !!technique.objective
        )
      ),
      map((techniques) => this.techniqueToPeriodEvent(techniques))
    );
  }

  private techniqueToPeriodEvent(
    technique: {
      technique: BonsaiTechnique;
      objective: BonsaiObjective;
      mapper: TechniqueMapper;
    }[]
  ): PeriodEvent[] {
    return technique.flatMap((technique) => {
      const periodsForTechnique = technique.mapper.period
        .map((period): PeriodEvent => {
          const months = periodToMonth(period);
          return {
            startMonth: months[0],
            endMonth: months[months.length - 1],
            eventId: technique.mapper.technique.id + period,
            text:
              technique.technique.display_name ??
              technique.technique.short_name,
            category: technique.technique.category ?? 'other',
            objective:
              technique.objective.display_name ??
              technique.objective.short_name,
          };
        })
        .sort((a, b) => a.startMonth - b.startMonth);

      // Merge periods if they are contiguous
      return periodsForTechnique.reduce((acc, period) => {
        const last = acc[acc.length - 1];
        if (last && last.endMonth >= period.startMonth) {
          last.endMonth = period.endMonth;
        } else {
          acc.push(period);
        }
        return acc;
      }, [] as PeriodEvent[]);
    });
  }
}
