import { Component } from '@angular/core';
import { NonNullableFormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, take } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { BonsaiStage, PeriodEnum } from 'swagger-client';
import { EntityForm, EntityType } from '../../entity-form';

@Component({
  selector: 'app-stage-form',
  templateUrl: './stage-form.component.html',
  styleUrls: ['./stage-form.component.scss'],
})
export class StageFormComponent extends EntityForm<BonsaiStage> {
  protected entityType: EntityType = 'stage';

  public entityForm = this.fb.group({
    display_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    description: this.fb.control<string | undefined>(undefined),
    global_period: this.fb.control<PeriodEnum[]>([]),
  });

  public periodOptions: { value: PeriodEnum; label: string }[] = Object.keys(
    PeriodEnum
  ).map((key) => {
    const stringKey = PeriodEnum[key as keyof typeof PeriodEnum];
    return {
      value: stringKey,
      label: AdviceService.periodIdToName(stringKey) ?? '',
    };
  });

  constructor(
    private adviceService: AdviceService,
    fb: NonNullableFormBuilder,
    route: ActivatedRoute,
    router: Router
  ) {
    super(fb, route, router);
  }

  initializeEntity(entityId: string): void {
    this.adviceService
      .getStage(entityId)
      .pipe(take(1))
      .subscribe((advice) => {
        this.combinedForm.patchValue({
          ...advice,
        });
      });
  }
  deleteEntity(shortName: string): Observable<any> {
    return this.adviceService.deleteStage(shortName);
  }
  updateEntity(entity: BonsaiStage): Observable<BonsaiStage> {
    return this.adviceService.updateStage(entity);
  }
  createEntity(entity: BonsaiStage): Observable<BonsaiStage> {
    return this.adviceService.createStage(entity);
  }

  formToEntity(): BonsaiStage | undefined {
    const commonFields = this.getCommonFieldsFromForm();
    const display_name = this.entityForm.controls.display_name.value ?? '';
    const description = this.entityForm.controls.description.value ?? '';
    const global_period =
      this.entityForm.controls.global_period.value ?? PeriodEnum._00;

    console.log(this.entityForm.controls);

    return {
      ...commonFields,
      display_name,
      description,
      global_period,
    };
  }
}
