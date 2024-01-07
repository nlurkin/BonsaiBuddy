import { Injectable } from '@angular/core';
import { createStore } from '@ngneat/elf';
import {
  addEntities,
  selectAllEntities,
  selectEntity,
  selectEntityByPredicate,
  setEntities,
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
} from 'rxjs';
import { AdvicesAPI, BonsaiTechnique } from 'swagger-client';

const techniqueStore = createStore(
  { name: 'techniques' },
  withEntities<BonsaiTechnique>()
);

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
}
