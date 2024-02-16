import { Component, OnInit, ViewChild } from '@angular/core';
import {
  FormControl,
  FormGroup,
  NonNullableFormBuilder,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Table } from 'primeng/table';
import { BehaviorSubject, Observable, map, take, tap } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import {
  BasicTreeInfo,
  TreeInfoService,
} from 'src/app/Services/tree-info.service';
import { bsonIdNull } from 'src/app/constants';
import { RouterURL } from 'src/app/types';
import { allPeriodIds } from 'src/app/utils';
import { PeriodEnum, TechniqueMapper } from 'swagger-client';
import {
  InputType,
  SelectOption,
} from '../../Generic/text-input/custom-input.component';

type TechniqueMapperGroupControls = FormGroup<{
  oid: FormControl<string | undefined>;
  comment: FormControl<string | undefined>;
  technique: FormControl<string | undefined>;
  objective: FormControl<string | undefined>;
  stage: FormControl<string[]>;
  period: FormControl<PeriodEnum[]>;
}>;
type TechniqueMapperGroup = {
  [oid: string]: TechniqueMapperGroupControls;
};

@Component({
  selector: 'app-tree-form',
  templateUrl: './tree-form.component.html',
  styleUrls: ['./tree-form.component.scss'],
})
export class TreeFormComponent implements OnInit {
  @ViewChild('techniqueDataTable', { static: true }) dataTable!: Table;

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
  public formTechniques = this.fb.group<TechniqueMapperGroup>({});
  public formTechniquesControlList$ = new BehaviorSubject<
    TechniqueMapperGroupControls[]
  >([]);

  private treeIdName: BehaviorSubject<string | undefined> = new BehaviorSubject<
    string | undefined
  >(undefined);
  private isCreating = false;

  public readonly techniqueOptions$: Observable<SelectOption[]> =
    this.adviceService.getTechniques().pipe(
      take(1),
      map((techniques) =>
        techniques
          .filter((technique) => technique.display_name !== undefined)
          .map((t): SelectOption => ({ label: t.display_name!, value: t.id }))
      )
    );

  public readonly objectiveOptions$: Observable<SelectOption[]> =
    this.adviceService.getObjectives().pipe(
      take(1),
      map((objectives) =>
        objectives
          .filter((objective) => objective.display_name !== undefined)
          .map((o): SelectOption => ({ label: o.display_name!, value: o.id }))
      )
    );

  public readonly stageOptions$: Observable<SelectOption[]> = this.adviceService
    .getStages()
    .pipe(
      take(1),
      map((stages) =>
        stages
          .filter((stage) => stage.display_name !== undefined)
          .map((s): SelectOption => ({ label: s.display_name!, value: s.id }))
      )
    );

  public readonly periodOptions: SelectOption[] = Array.from(
    allPeriodIds()
  ).map(([key, value]) => ({ label: value, value: key }));

  constructor(
    private fb: NonNullableFormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private treeService: TreeInfoService,
    private adviceService: AdviceService
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
      .pipe(
        take(1),
        tap((tree) => {
          const { techniques, ...baseTree } = tree;
          this.form.patchValue({
            ...baseTree,
          });
        }),
        map((tree): TechniqueMapperGroupControls[] => {
          return tree.techniques.map((technique, rowIndex) => {
            const techniqueGroup: TechniqueMapperGroupControls = this.fb.group({
              oid: this.fb.control<string | undefined>(technique.oid),
              comment: this.fb.control<string | undefined>(technique.comment),
              technique: this.fb.control<string | undefined>(
                technique.technique.id,
                [Validators.required]
              ),
              objective: this.fb.control<string | undefined>(
                technique.objective.id,
                [Validators.required]
              ),
              stage: this.fb.control<string[]>(
                technique.stage.map((s) => s.id)
              ),
              period: this.fb.control<PeriodEnum[]>(technique.period),
            });
            this.formTechniques.addControl(technique.oid, techniqueGroup);
            return techniqueGroup;
          });
        })
      )
      .subscribe((controls) => {
        this.formTechniquesControlList$.next(controls);
      });
  }

  public onSubmitBaseTree(): void {
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

  public onRowEditSave(oid: string): void {
    console.log(oid, this.formTechniques.controls[oid]);
  }

  public onRowEditCancel(oid: string): void {
    this.formTechniques.controls[oid].reset();
  }

  public onRowEditInit(oid: string): void {
    const formData: TechniqueMapperGroupControls =
      this.formTechniques.controls[oid];
    if (this.dataTable.isRowExpanded(formData))
      this.dataTable.toggleRow(formData);
  }

  public onRowClone(oid: string): void {
    const form = this.formTechniques.controls[
      oid
    ] as TechniqueMapperGroupControls;
    const newOid = `${bsonIdNull}-${this.numberOfNewLines++}`;
    const clone = form.getRawValue();
    const techniqueGroup: TechniqueMapperGroupControls = this.fb.group({
      oid: this.fb.control<string | undefined>(newOid),
      comment: this.fb.control<string | undefined>(clone.comment),
      technique: this.fb.control<string | undefined>(clone.technique, [
        Validators.required,
      ]),
      objective: this.fb.control<string | undefined>(clone.objective, [
        Validators.required,
      ]),
      stage: this.fb.control<string[]>(clone.stage.map((s) => s)),
      period: this.fb.control<PeriodEnum[]>(clone.period),
    });
    this.formTechniques.addControl(newOid, techniqueGroup);
    this.formTechniquesControlList$.next([
      ...this.formTechniquesControlList$.value,
      this.formTechniques.controls[newOid] as TechniqueMapperGroupControls,
    ]);
  }

  public deeleteSelected(): void {
    const selected = this.dataTable.selectionKeys as Record<string, number>;
    const oidToRemove = Object.keys(selected);
    const group = this.formTechniques as FormGroup;
    oidToRemove.forEach((s) => group.removeControl(s));
    this.formTechniquesControlList$.next(
      this.formTechniquesControlList$.value.filter(
        (c) => !oidToRemove.includes(c.controls.oid.value ?? '')
      )
    );
  }

  private numberOfNewLines = 0;
  public addTechnique(): void {
    const oid = `${bsonIdNull}-${this.numberOfNewLines++}`;
    const group: TechniqueMapperGroupControls = this.fb.group({
      oid: this.fb.control<string | undefined>(oid),
      comment: this.fb.control<string | undefined>(undefined),
      technique: this.fb.control<string | undefined>(undefined, [
        Validators.required,
      ]),
      objective: this.fb.control<string | undefined>(undefined, [
        Validators.required,
      ]),
      stage: this.fb.control<string[]>([]),
      period: this.fb.control<PeriodEnum[]>([]),
    });
    this.formTechniques.addControl(oid, group);
    this.formTechniquesControlList$.next([
      ...this.formTechniquesControlList$.value,
      group,
    ]);
    this.dataTable.editingRowKeys = {
      ...this.dataTable.editingRowKeys,
      [oid]: true,
    };
  }

  private techniqueFormToEntity(
    form: TechniqueMapperGroupControls
  ): TechniqueMapper | undefined {
    if (!this.formTechniques.valid) return undefined;
    const values = form.getRawValue();
    const oid = values.oid?.includes(bsonIdNull) ? bsonIdNull : values.oid;
    return {
      oid: oid ?? bsonIdNull,
      comment: values.comment ?? '',
      // Validity of these values is guaranteed by the form validation
      technique: { classname: 'BonsaiTechnique', id: values.technique! },
      objective: { classname: 'BonsaiObjective', id: values.objective! },
      stage: values.stage.map((s) => ({ classname: 'BonsaiStage', id: s })),
      period: values.period,
    };
  }

  private techniqueFormsToEntities(): TechniqueMapper[] | undefined {
    if (!this.formTechniques.valid) return undefined;
    return Object.values(this.formTechniques.controls)
      .map((form: TechniqueMapperGroupControls) =>
        this.techniqueFormToEntity(form)
      )
      .filter((t): t is TechniqueMapper => t !== undefined);
  }

  public onSubmitTechniques(): void {
    const treeId = this.treeIdName.value;
    if (treeId) {
      const techniques = this.techniqueFormsToEntities();
      console.log(techniques);
      if (techniques) {
        this.treeService
          .updateTechniqueMapping(treeId, techniques)
          .pipe(take(1))
          .subscribe(() => {
            this.router.navigate(['..'], { relativeTo: this.route });
          });
      }
    }
  }
}
