import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as _ from 'lodash';
import { Observable, combineLatest, map, switchMap } from 'rxjs';
import { AdviceService, BonsaiEntity } from 'src/app/Services/advice.service';
import { TreeInfoService } from 'src/app/Services/tree-info.service';
import { filterNullish } from 'src/app/rxjs-util';
import { standardEntitySort } from 'src/app/utils';
import {
  BonsaiStage,
  BonsaiTechnique,
  LazyReferenceField,
  TechniqueMapper,
} from 'swagger-client';

@Component({
  selector: 'app-tree-detail',
  templateUrl: './tree-detail.component.html',
  styleUrls: ['./tree-detail.component.scss'],
})
export class TreeDetailComponent {
  public readonly tree$ = this.route.paramMap.pipe(
    map((params) => params.get('id')),
    filterNullish(),
    switchMap((id) => this.treeService.getTreeInfo(id))
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


  constructor(
    public route: ActivatedRoute,
    public treeService: TreeInfoService,
    public adviceService: AdviceService
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
}
