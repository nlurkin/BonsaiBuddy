import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject, Observable, map, take } from 'rxjs';
import {
  InputType,
  SelectOption,
} from 'src/app/Components/Generic/text-input/custom-input.component';
import { AdviceService } from 'src/app/Services/advice.service';
import { BonsaiTechnique } from 'swagger-client';

@Component({
  selector: 'app-technique-form',
  templateUrl: './technique-form.component.html',
  styleUrls: ['./technique-form.component.scss'],
})
export class TechniqueFormComponent implements OnInit {
  public InputType = InputType;

  public techniqueForm = this.fb.group({
    short_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    id: this.fb.control<string | undefined>(undefined),
    display_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    description: this.fb.control<string | undefined>(undefined),
    category: this.fb.control<string | undefined>(undefined),
    published: this.fb.control<boolean>(false),
    sequence: this.fb.control<number | undefined>(99),
    delete: this.fb.control<boolean>(false),
  });

  private techniqueIdName: BehaviorSubject<string | undefined> =
    new BehaviorSubject<string | undefined>(undefined);
  private techniqueCategories$ = this.adviceService.getTechniqueCategories();

  public techniqueCategoriesOptoins$: Observable<SelectOption[]> =
    this.techniqueCategories$.pipe(
      map((categories) =>
        categories.map((category) => ({
          label: category,
          value: category.toLowerCase(),
        }))
      )
    );

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private adviceService: AdviceService
  ) {
    this.route.params.pipe(take(1)).subscribe((params) => {
      this.techniqueIdName.next(params['id']);
    });
  }

  ngOnInit(): void {
    this.techniqueForm.controls.short_name.disable();
    const techniqueId = this.techniqueIdName.value;
    if (techniqueId) {
      this.adviceService
        .getTechnique(techniqueId)
        .pipe(take(1))
        .subscribe((advice) => {
          this.techniqueForm.patchValue({
            ...advice,
          });
        });
    }
  }

  public onSubmit(): void {
    console.log(this.techniqueForm.value);

    if (this.techniqueForm.controls.delete.value) {
      // Delete
    } else {
      const entity = this.formToEntity();
      // Update

      if (entity) this.adviceService.updateTechnique(entity);

      //New
    }
  }

  private formToEntity(): BonsaiTechnique | undefined {
    if (!this.techniqueForm.valid) return undefined;

    const short_name = this.techniqueForm.controls.short_name.value ?? '';
    const id = this.techniqueForm.controls.id.value ?? '';
    const display_name = this.techniqueForm.controls.display_name.value ?? '';
    const description = this.techniqueForm.controls.description.value ?? '';
    const category = this.techniqueForm.controls.category.value ?? '';
    const published = this.techniqueForm.controls.published.value ?? false;
    const sequence = this.techniqueForm.controls.sequence.value ?? 99;

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
