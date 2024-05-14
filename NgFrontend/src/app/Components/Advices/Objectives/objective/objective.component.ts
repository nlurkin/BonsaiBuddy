import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, map, switchMap } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { UserService } from 'src/app/Services/user.service';
import { filterNullish } from 'src/app/rxjs-util';
import { BonsaiObjective } from 'swagger-client';

@Component({
  selector: 'app-objective',
  templateUrl: './objective.component.html',
  styleUrls: ['./objective.component.scss'],
})
export class ObjectiveComponent {
  public readonly objective$: Observable<BonsaiObjective | undefined> =
    this.route.paramMap.pipe(
      map((params) => params.get('id')),
      filterNullish(),
      switchMap((id) => this.adviceService.getObjective(id))
    );

  public canEdit$: Observable<boolean> =
    this.userService.currentUserHasPermissions('BonsaiAdvice.change_content');

  constructor(
    private adviceService: AdviceService,
    private userService: UserService,
    private route: ActivatedRoute
  ) {}
}
