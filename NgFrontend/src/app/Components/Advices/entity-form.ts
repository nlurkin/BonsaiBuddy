import { BonsaiEntity } from 'src/app/Services/advice.service';

import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject, Observable, take } from 'rxjs';
import { RouterURL } from 'src/app/types';
import { InputType } from '../Generic/text-input/custom-input.component';

export type EntityType = 'technique' | 'objective';

@Component({
  selector: 'app-entity-form',
  template: '',
})
export abstract class EntityForm<T extends BonsaiEntity> {
  // Abstract properties
  abstract entityForm: FormGroup<any>;
  protected abstract entityType: EntityType;

  //Abstract methods
  abstract initializeEntity(entityId: string): void;
  abstract formToEntity(): T | undefined;
  abstract deleteEntity(shortName: string): Observable<any>;
  abstract updateEntity(entity: T): Observable<T>;
  abstract createEntity(entity: T): Observable<T>;

  public InputType = InputType;
  protected commonControls = this.fb.group({
    short_name: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(200),
    ]),
    id: this.fb.control<string | undefined>(undefined),
    published: this.fb.control<boolean>(false),
    delete: this.fb.control<boolean>(false),
  });
  protected combinedForm!: FormGroup;

  private entityIdName: BehaviorSubject<string | undefined> =
    new BehaviorSubject<string | undefined>(undefined);
  private isCreating = false;

  protected constructor(
    protected fb: FormBuilder,
    protected route: ActivatedRoute,
    protected router: Router
  ) {
    this.route.params.pipe(take(1)).subscribe((params) => {
      this.entityIdName.next(params['id']);
    });
  }

  ngOnInit(): void {
    this.combinedForm = new FormGroup({
      ...this.commonControls.controls,
      ...this.entityForm.controls,
    });
    const entityId = this.entityIdName.value;
    if (entityId) {
      this.commonControls.controls.short_name.disable();
      this.initializeEntity(entityId);
    } else {
      this.isCreating = true;
    }
  }

  public onSubmit(): void {
    const shortName = this.commonControls.controls.short_name.value;
    if (
      this.commonControls.controls.delete.value &&
      shortName &&
      !this.isCreating
    ) {
      // Delete
      this.done(this.deleteEntity(shortName), ['advices']);
    } else {
      const entity = this.getEntityFromForm();
      // Update or create
      if (entity && !this.isCreating)
        this.done(this.updateEntity(entity), ['..']);
      else if (entity && this.isCreating)
        this.done(this.createEntity(entity), [
          `advices/${this.entityType}`,
          entity.short_name,
        ]);
    }
  }

  public done(updateObs: Observable<any>, returnUrl: RouterURL): void {
    updateObs.pipe(take(1)).subscribe(() =>
      this.router.navigate(returnUrl, {
        relativeTo: returnUrl.some((segment) => segment.includes('..'))
          ? this.route
          : undefined,
      })
    );
  }

  private getEntityFromForm(): T | undefined {
    if (!this.entityForm.valid) return undefined;

    return this.formToEntity();
  }
}
