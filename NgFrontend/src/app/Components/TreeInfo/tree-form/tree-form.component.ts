import { Component, OnInit } from '@angular/core';
import { NonNullableFormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject, Observable, take } from 'rxjs';
import {
  BasicTreeInfo,
  TreeInfoService,
} from 'src/app/Services/tree-info.service';
import { bsonIdNull } from 'src/app/constants';
import { RouterURL } from 'src/app/types';
import { InputType } from '../../Generic/text-input/custom-input.component';

@Component({
  selector: 'app-tree-form',
  templateUrl: './tree-form.component.html',
  styleUrls: ['./tree-form.component.scss'],
})
export class TreeFormComponent implements OnInit {
  public InputType = InputType;
  public form = this.fb.group({
    id: this.fb.control<string | undefined>(undefined),
    display_name: this.fb.control<string | undefined>(undefined),
    latin_name: this.fb.control<string | undefined>(undefined),
    description: this.fb.control<string | undefined>(undefined),
    placement: this.fb.control<string | undefined>(undefined),
    watering: this.fb.control<string | undefined>(undefined),
    fertilizing: this.fb.control<string | undefined>(undefined),
    pruning_wiring: this.fb.control<string | undefined>(undefined),
    repotting: this.fb.control<string | undefined>(undefined),
    propagation: this.fb.control<string | undefined>(undefined),
    pests: this.fb.control<string | undefined>(undefined),
    published: this.fb.control<boolean>(false),
    delete: this.fb.control<boolean>(false),
  });

  private treeIdName: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >(undefined);
  private isCreating = false;

  constructor(
    private fb: NonNullableFormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private treeService: TreeInfoService
  ) {
    this.route.params.pipe(take(1)).subscribe((params) => {
      this.treeIdName.next(params['id']);
    });
  }

  ngOnInit(): void {
    const treeId = this.treeIdName.value;
    if (treeId) {
      this.form.controls.display_name.disable();
      this.initializeEntity(treeId);
    } else {
      this.isCreating = true;
    }
  }

  public initializeEntity(entityId: string): void {
    this.treeService
      .getTreeInfo(entityId)
      .pipe(take(1))
      .subscribe((tree) => {
        this.form.patchValue({
          ...tree,
        });
      });
  }

  public onSubmit(): void {
    const name = this.form.controls.display_name.value?.toLowerCase() ?? '';

    if (this.form.controls.delete.value && name && !this.isCreating) {
      // Delete
      this.done(this.treeService.deleteTreeInfo(name), ['treeinfo']);
    } else {
      const entity = this.getEntityFromForm();
      // Update or create
      if (entity && !this.isCreating)
        this.done(this.treeService.updateBasicTreeInfo(name, entity), ['..']);
      else if (entity && this.isCreating)
        this.done(
          this.treeService.createTreeInfo({ ...entity, techniques: [] }),
          ['treeinfo', entity.name]
        );
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

  private getEntityFromForm(): BasicTreeInfo | undefined {
    if (!this.form.valid) return undefined;

    return {
      id: this.form.controls.id.value ?? bsonIdNull,
      name: this.form.controls.display_name.value?.toLowerCase() ?? '',
      display_name: this.form.controls.display_name.value ?? '',
      latin_name: this.form.controls.latin_name.value ?? '',
      description: this.form.controls.description.value ?? '',
      placement: this.form.controls.placement.value ?? '',
      watering: this.form.controls.watering.value ?? '',
      fertilizing: this.form.controls.fertilizing.value ?? '',
      pruning_wiring: this.form.controls.pruning_wiring.value ?? '',
      repotting: this.form.controls.repotting.value ?? '',
      propagation: this.form.controls.propagation.value ?? '',
      pests: this.form.controls.pests.value ?? '',
      published: this.form.controls.published.value ?? false,
    };
  }
}
