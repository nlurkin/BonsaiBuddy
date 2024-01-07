import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, map, switchMap } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { filterNullish } from 'src/app/utils';
import { BonsaiTechnique } from 'swagger-client';

@Component({
  selector: 'app-technique',
  templateUrl: './technique.component.html',
  styleUrls: ['./technique.component.scss'],
})
export class TechniqueComponent {
  public readonly technique$: Observable<BonsaiTechnique | undefined> =
    this.route.paramMap.pipe(
      map((params) => params.get('id')),
      filterNullish(),
      switchMap((id) => this.adviceService.getTechnique(id))
    );

  constructor(
    private adviceService: AdviceService,
    private route: ActivatedRoute
  ) {}
}
