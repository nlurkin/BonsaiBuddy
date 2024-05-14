import { Component } from '@angular/core';
import { NonNullableFormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, take } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { BonsaiObjective } from 'swagger-client';
import { EntityForm, EntityType } from '../../entity-form';

@Component({
  selector: 'app-objective-form',
  templateUrl: './objective-form.component.html',
  styleUrls: ['./objective-form.component.scss'],
})
export class ObjectiveFormComponent extends EntityForm<BonsaiObjective> {
  protected entityType: EntityType = 'objective';

  public entityForm = this.fb.group({
    display_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    description: this.fb.control<string | undefined>(undefined),
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
      .getObjective(entityId)
      .pipe(take(1))
      .subscribe((advice) => {
        this.combinedForm.patchValue({
          ...advice,
        });
      });
  }
  deleteEntity(shortName: string): Observable<any> {
    return this.adviceService.deleteObjective(shortName);
  }
  updateEntity(entity: BonsaiObjective): Observable<BonsaiObjective> {
    return this.adviceService.updateObjective(entity);
  }
  createEntity(entity: BonsaiObjective): Observable<BonsaiObjective> {
    return this.adviceService.createObjective(entity);
  }

  formToEntity(): BonsaiObjective | undefined {
    const commonFields = this.getCommonFieldsFromForm();
    const display_name = this.entityForm.controls.display_name.value ?? '';
    const description = this.entityForm.controls.description.value ?? '';

    return {
      ...commonFields,
      display_name,
      description,
    };
  }
}
