import { Component } from '@angular/core';
import { NonNullableFormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, map, take } from 'rxjs';
import { SelectOption } from 'src/app/Components/Generic/text-input/custom-input.component';
import { AdviceService } from 'src/app/Services/advice.service';
import { bsonIdNull } from 'src/app/constants';
import { BonsaiTechnique } from 'swagger-client';
import { EntityForm, EntityType } from '../../entity-form';

@Component({
  selector: 'app-technique-form',
  templateUrl: './technique-form.component.html',
  styleUrls: ['./technique-form.component.scss'],
})
export class TechniqueFormComponent extends EntityForm<BonsaiTechnique> {
  protected entityType: EntityType = 'technique';

  public entityForm = this.fb.group({
    display_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    description: this.fb.control<string | undefined>(undefined),
    category: this.fb.control<string | undefined>(undefined),
    sequence: this.fb.control<number | undefined>(99),
  });

  private techniqueCategories$ = this.adviceService.getTechniqueCategories();

  public techniqueCategoriesOptions$: Observable<SelectOption[]> =
    this.techniqueCategories$.pipe(
      map((categories) =>
        categories.map((category) => ({
          label: category,
          value: category.toLowerCase(),
        }))
      )
    );

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
      .getTechnique(entityId)
      .pipe(take(1))
      .subscribe((advice) => {
        this.combinedForm.patchValue({
          ...advice,
        });
      });
  }
  deleteEntity(shortName: string): Observable<any> {
    return this.adviceService.deleteTechnique(shortName);
  }
  updateEntity(entity: BonsaiTechnique): Observable<BonsaiTechnique> {
    return this.adviceService.updateTechnique(entity);
  }
  createEntity(entity: BonsaiTechnique): Observable<BonsaiTechnique> {
    return this.adviceService.createTechnique(entity);
  }

  formToEntity(): BonsaiTechnique | undefined {
    const id = this.commonControls.controls.id.value ?? bsonIdNull;
    const short_name = this.commonControls.controls.short_name.value ?? '';
    const display_name = this.entityForm.controls.display_name.value ?? '';
    const description = this.entityForm.controls.description.value ?? '';
    const category = this.entityForm.controls.category.value ?? '';
    const published = this.commonControls.controls.published.value ?? false;
    const sequence = this.entityForm.controls.sequence.value ?? 99;

    return {
      short_name,
      id,
      display_name,
      description,
      category,
      published,
      sequence,
    };
  }
}
