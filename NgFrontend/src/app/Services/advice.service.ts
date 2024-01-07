import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AdvicesAPI, BonsaiTechnique } from 'swagger-client';

@Injectable({
  providedIn: 'root',
})
export class AdviceService {
  constructor(private techniqueApiService: AdvicesAPI) {}

  public getTechniques(): Observable<BonsaiTechnique[]> {
    return this.techniqueApiService.advicesList();
  }

  public getTechnique(id: string): Observable<BonsaiTechnique> {
    return this.techniqueApiService.advicesRetrieve(id);
  }

  public getTechniqueCategories(): Observable<string[]> {
    return this.techniqueApiService.advicesTechniquesCategoriesRetrieve();
  }
}
