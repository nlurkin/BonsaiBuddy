import { Injectable } from '@angular/core';
import { Store, createStore } from '@ngneat/elf';
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
import {
  AdvicesAPI,
  BonsaiObjective,
  BonsaiStage,
  BonsaiTechnique,
} from 'swagger-client';

const techniqueStore = createStore(
  { name: 'techniques' },
  withEntities<BonsaiTechnique>()
);
type StoreType<T> = Store<
  {
    name: string;
    state: { entities: Record<string, T>; ids: string[] };
    config: { idKey: 'id' };
  },
  { entities: Record<string, T>; ids: string[] }
>;

type StoreCommands = 'update' | 'create' | 'delete';
type BonsaiEntity = BonsaiTechnique | BonsaiObjective | BonsaiStage;

@Injectable({
  providedIn: 'root',
})
export class AdviceService {
  private readonly refreshTechnique$: BehaviorSubject<void> =
    new BehaviorSubject<void>(undefined); // To force the refresh of the store

  constructor(private techniqueApiService: AdvicesAPI) {}

  /**
   * Generic methods
   */
  private initializeStore<T>(
    refresh$: BehaviorSubject<void>,
    retrieveFn: () => Observable<T[]>,
    store: StoreType<T>
  ): Observable<boolean> {
    return refresh$.pipe(
      switchMap(() =>
        retrieveFn
          .bind(this.techniqueApiService)()
          .pipe(
            take(1),
            map((entities) => {
              store.update(setEntities(entities));
              return true;
            })
          )
      ),
      shareReplay(1)
    );
  }
  private fetchEntity<T extends BonsaiEntity>(
    id: string,
    retrieveFn: (id: string) => Observable<T>,
    store: StoreType<T>
  ): Observable<T | undefined> {
    retrieveFn
      .bind(this.techniqueApiService)(id)
      .pipe(take(1))
      .subscribe((entity: T) => {
        store.update(addEntities(entity));
      });
    return store.pipe(selectEntity(id));
  }

  public getEntity<T extends BonsaiEntity>(
    entity_short_name: string,
    retrieveFn: (id: string) => Observable<T>,
    storeInitialized$: Observable<boolean>,
    store: StoreType<T>
  ): Observable<T | undefined> {
    return storeInitialized$.pipe(
      switchMap(() =>
        store.pipe(
          selectEntityByPredicate(
            ({ short_name }) => short_name === entity_short_name
          ),
          switchMap((entity) =>
            entity
              ? of(entity)
              : this.fetchEntity<T>(entity_short_name, retrieveFn, store)
          )
        )
      )
    );
  }

  public updateEntity<T extends BonsaiEntity>(
    entity: T,
    updateFn: (short_name: string, e: T) => Observable<T>,
    store: StoreType<T>
  ): Observable<T> {
    return updateFn
      .bind(this.techniqueApiService)(entity.short_name, entity)
      .pipe(
        take(1),
        tap((updatedEntity) =>
          this.updateStore<T>(updatedEntity, store, 'update')
        )
      );
  }

  public createEntity<T extends BonsaiEntity>(
    entity: T,
    createFn: (e: T) => Observable<T>,
    store: StoreType<T>
  ): Observable<T> {
    return createFn
      .bind(this.techniqueApiService)(entity)
      .pipe(
        take(1),
        tap((entity) => this.updateStore<T>(entity, store, 'create'))
      );
  }

  public deleteEntity<T extends BonsaiEntity>(
    entity_short_name: string,
    deleteFn: (short_name: string) => Observable<any>,
    store: StoreType<T>
  ): Observable<any> {
    return deleteFn
      .bind(this.techniqueApiService)(entity_short_name)
      .pipe(
        take(1),
        tap(() => this.deleteFromStore<T>(entity_short_name, store))
      );
  }

  private updateStore<T extends BonsaiEntity>(
    technique: T,
    store: StoreType<T>,
    command: StoreCommands
  ): void {
    if (command === 'update')
      store.update(
        updateEntitiesByPredicate(
          ({ short_name }) => short_name === technique.short_name,
          () => technique
        )
      );
    else if (command === 'create') store.update(addEntities([technique]));
    else if (command === 'delete')
      this.deleteFromStore<T>(technique.short_name, store);
  }

  private deleteFromStore<T extends BonsaiEntity>(
    entity_short_name: string,
    store: StoreType<T>
  ): void {
    store.update(
      deleteEntitiesByPredicate(
        ({ short_name }) => short_name === entity_short_name
      )
    );
  }

  /**
   * Interactions with the API
   */
  private initializedTechniqueStore$ = this.initializeStore(
    this.refreshTechnique$,
    this.techniqueApiService.advicesTechniquesList,
    techniqueStore
  );

  private fetchTechnique(id: string): Observable<BonsaiTechnique | undefined> {
    return this.fetchEntity<BonsaiTechnique>(
      id,
      this.techniqueApiService.advicesTechniquesRetrieve,
      techniqueStore
    );
  }

  }

  public getTechniqueCategories(): Observable<string[]> {
    return this.techniqueApiService.advicesTechniquesCategoriesRetrieve();
  }

  public updateTechnique(
    technique: BonsaiTechnique
  ): Observable<BonsaiTechnique> {
    return this.updateEntity(
      technique,
      this.techniqueApiService.advicesTechniquesUpdate,
      techniqueStore
    );
  }

  public createTechnique(
    technique: BonsaiTechnique
  ): Observable<BonsaiTechnique> {
    return this.createEntity(
      technique,
      this.techniqueApiService.advicesTechniquesCreate,
      techniqueStore
    );
  }

  public deleteTechnique(technique_short_name: string): Observable<any> {
    return this.deleteEntity(
      technique_short_name,
      this.techniqueApiService.advicesTechniquesDestroy,
      techniqueStore
    );
  }

  }

  /**
   * Interactions with the store
   */
  public getTechniques(): Observable<BonsaiTechnique[]> {
    return this.initializedTechniqueStore$.pipe(
      switchMap(() => techniqueStore.pipe(selectAllEntities()))
    );
  }

  public getTechnique(name: string): Observable<BonsaiTechnique | undefined> {
    return this.getEntity<BonsaiTechnique>(
      name,
      this.techniqueApiService.advicesTechniquesRetrieve,
      this.initializedTechniqueStore$,
      techniqueStore
    );
  }

}
