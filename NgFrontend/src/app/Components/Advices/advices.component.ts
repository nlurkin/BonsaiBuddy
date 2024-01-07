import { Component } from '@angular/core';
import { Observable, map } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import * as _ from 'lodash';
import { BonsaiTechnique } from 'swagger-client';

@Component({
  selector: 'app-advices',
  templateUrl: './advices.component.html',
  styleUrls: ['./advices.component.scss'],
})
export class AdvicesComponent {
  public readonly techniqueCategories$: Observable<string[]> =
    this.adviceService.getTechniqueCategories();
  public readonly techniquesByCategories$: Observable<
    _.Dictionary<BonsaiTechnique[]>
  > = this.adviceService
    .getTechniques()
    .pipe(
      map((techniques) =>
        _.groupBy(techniques, (technique) => technique.category)
      )
    );

  constructor(private adviceService: AdviceService) {}
}
