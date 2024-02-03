import { Pipe, PipeTransform } from '@angular/core';
import { periodIdToName } from './utils';

@Pipe({
  name: 'periodIdToName',
})
export class PeriodIdToNamePipe implements PipeTransform {
  transform(periodId: string | string[] | undefined): unknown {
    if (!periodId) return '';
    if (Array.isArray(periodId)) {
      return periodId.map(periodIdToName).join(', ');
    }
    return periodIdToName(periodId);
  }
}
