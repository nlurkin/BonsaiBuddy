import { Pipe, PipeTransform } from '@angular/core';
import { AdviceService } from './Services/advice.service';
import { Observable, map, of } from 'rxjs';

@Pipe({
  name: 'entityIdToName',
})
export class EntityIdToNamePipe implements PipeTransform {
  constructor(private adviceService: AdviceService) {}

  transform(
    oid: string | undefined,
    entityType: 'technique' | 'objective' | 'stage'
  ): Observable<string> {
    if (!oid) return of('');
    if (entityType === 'technique') {
      return this.adviceService
        .getTechniqueById(oid)
        .pipe(map((t) => t?.display_name ?? `nf: oid`));
    } else if (entityType === 'objective') {
      return this.adviceService
        .getObjectiveById(oid)
        .pipe(map((o) => o?.display_name ?? oid));
    } else if (entityType === 'stage') {
      return this.adviceService
        .getStageById(oid)
        .pipe(map((s) => s?.display_name ?? oid));
    }
    return of('');
  }
}
