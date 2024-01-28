import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, map, switchMap } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { filterNullish } from 'src/app/utils';
import { BonsaiStage } from 'swagger-client';

@Component({
  selector: 'app-stage',
  templateUrl: './stage.component.html',
  styleUrls: ['./stage.component.scss'],
})
export class StageComponent {
  public readonly stage$: Observable<BonsaiStage | undefined> =
    this.route.paramMap.pipe(
      map((params) => params.get('id')),
      filterNullish(),
      switchMap((id) => this.adviceService.getStage(id))
    );

  constructor(
    private adviceService: AdviceService,
    private route: ActivatedRoute
  ) {}
}
