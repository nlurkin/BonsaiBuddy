import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, map, switchMap } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { UserService } from 'src/app/Services/user.service';
import { filterNullish } from 'src/app/utils';
import { BonsaiStage } from 'swagger-client';

type BonsaiStageWithPeriodNames = BonsaiStage & {
  global_period_names: string[];
};

@Component({
  selector: 'app-stage',
  templateUrl: './stage.component.html',
  styleUrls: ['./stage.component.scss'],
})
export class StageComponent {
  public readonly stage$: Observable<BonsaiStageWithPeriodNames | undefined> =
    this.route.paramMap.pipe(
      map((params) => params.get('id')),
      filterNullish(),
      switchMap((id) => this.adviceService.getStage(id)),
      map((stage) => {
        if (!stage) {
          return undefined;
        }
        return {
          ...stage,
          global_period_names: stage.global_period.map(
            (p) => AdviceService.periodIdToName(p) ?? p
          ),
        };
      })
    );

  public canEdit$: Observable<boolean> =
    this.userService.currentUserHasPermissions('BonsaiAdvice.change_content');

  constructor(
    private adviceService: AdviceService,
    private userService: UserService,
    private route: ActivatedRoute
  ) {}
}
