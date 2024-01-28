import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, take } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { bsonIdNull } from 'src/app/constants';
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
    sequence: this.fb.control<number | undefined>(99),
  });

  constructor(
    private adviceService: AdviceService,
    fb: FormBuilder,
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
    const id = this.commonControls.controls.id.value ?? bsonIdNull;
    const short_name = this.commonControls.controls.short_name.value ?? '';
    const display_name = this.entityForm.controls.display_name.value ?? '';
    const description = this.entityForm.controls.description.value ?? '';
    const published = this.commonControls.controls.published.value ?? false;
    const sequence = this.entityForm.controls.sequence.value ?? 99;

    return {
      short_name,
      id,
      display_name,
      description,
      published,
      sequence,
    };
  }
}
