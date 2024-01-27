import { Injectable } from '@angular/core';
import { createStore } from '@ngneat/elf';
import {
  addEntities,
  deleteEntitiesByPredicate,
  selectAllEntities,
  selectEntity,
  selectEntityByPredicate,
  setEntities,
  updateEntitiesByPredicate,
  withEntities,
} from '@ngneat/elf-entities';
import {
  BehaviorSubject,
  Observable,
  map,
  of,
  shareReplay,
  switchMap,
  take,
  tap,
} from 'rxjs';
import { AdvicesAPI, BonsaiTechnique } from 'swagger-client';

const techniqueStore = createStore(
  { name: 'techniques' },
  withEntities<BonsaiTechnique>()
);

type StoreCommands = 'update' | 'create' | 'delete';

@Injectable({
  providedIn: 'root',
})
export class AdviceService {
  private readonly refresh$: BehaviorSubject<void> = new BehaviorSubject<void>(
    undefined
  ); // To force the refresh of the store

  constructor(private techniqueApiService: AdvicesAPI) {}

  /**
   * Interactions with the API
   */
  private initializedStore$: Observable<boolean> = this.refresh$.pipe(
    switchMap(() =>
      this.techniqueApiService.advicesTechniquesList().pipe(
        take(1),
        map((techniques) => {
          techniqueStore.update(setEntities(techniques));
          return true;
        })
      )
    ),
    shareReplay(1)
  );

  private fetchTechnique(id: string): Observable<BonsaiTechnique | undefined> {
    this.techniqueApiService
      .advicesTechniquesRetrieve(id)
      .pipe(take(1))
      .subscribe((techniques) => {
        techniqueStore.update(addEntities(techniques));
      });
    return techniqueStore.pipe(selectEntity(id));
  }

  public getTechniqueCategories(): Observable<string[]> {
    return this.techniqueApiService.advicesTechniquesCategoriesRetrieve();
  }

  public updateTechnique(
    technique: BonsaiTechnique
  ): Observable<BonsaiTechnique> {
    return this.techniqueApiService
      .advicesTechniquesUpdate(technique.short_name, technique)
      .pipe(
        take(1),
        tap((technique) => this.updateStore(technique, 'update'))
      );
  }

  public createTechnique(
    technique: BonsaiTechnique
  ): Observable<BonsaiTechnique> {
    return this.techniqueApiService.advicesTechniquesCreate(technique).pipe(
      take(1),
      tap((technique) => this.updateStore(technique, 'create'))
    );
  }

  public deleteTechnique(technique_short_name: string): Observable<any> {
    return this.techniqueApiService
      .advicesTechniquesDestroy(technique_short_name)
      .pipe(
        take(1),
        tap(() => this.deleteFromStore(technique_short_name))
      );
  }

  /**
   * Interactions with the store
   */
  public getTechniques(): Observable<BonsaiTechnique[]> {
    return this.initializedStore$.pipe(
      switchMap(() => techniqueStore.pipe(selectAllEntities()))
    );
  }

  public getTechnique(name: string): Observable<BonsaiTechnique | undefined> {
    return this.initializedStore$.pipe(
      switchMap(() =>
        techniqueStore.pipe(
          selectEntityByPredicate(({ short_name }) => short_name === name),
          switchMap((entity) =>
            entity ? of(entity) : this.fetchTechnique(name)
          )
        )
      )
    );
  }

  private updateStore(
    technique: BonsaiTechnique,
    command: StoreCommands
  ): void {
    if (command === 'update')
      techniqueStore.update(
        updateEntitiesByPredicate(
          ({ short_name }) => short_name === technique.short_name,
          () => technique
        )
      );
    else if (command === 'create')
      techniqueStore.update(addEntities([technique]));
    else if (command === 'delete') this.deleteFromStore(technique.short_name);
  }

  private deleteFromStore(technique_short_name: string): void {
    techniqueStore.update(
      deleteEntitiesByPredicate(
        ({ short_name }) => short_name === technique_short_name
      )
    );
  }
}
