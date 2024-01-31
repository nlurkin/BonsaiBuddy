import { Component } from '@angular/core';
import { NonNullableFormBuilder, Validators } from '@angular/forms';
import { combineLatestWith, map, take } from 'rxjs';
import { AdviceService } from 'src/app/Services/advice.service';
import { ToastingService } from 'src/app/Services/toasting.service';
import { TreeInfoService } from 'src/app/Services/tree-info.service';
import { UserService } from 'src/app/Services/user.service';
import { filterDefined } from 'src/app/rxjs-util';
import {
  InputType,
  SelectOption,
} from '../../Generic/text-input/custom-input.component';

@Component({
  selector: 'app-my-trees',
  templateUrl: './my-trees.component.html',
  styleUrls: ['./my-trees.component.scss'],
})
export class MyTreesComponent {
  public InputType = InputType;
  public form = this.fb.group({
    tree: this.fb.control<string | undefined>(undefined, [Validators.required]),
    objective: this.fb.control<string | undefined>(undefined, [
      Validators.required,
    ]),
  });

  private profileTrees$ = this.userService.getCurrentUserProfile().pipe(
    filterDefined(),
    map((user) => user.my_trees)
  );

  private allObjectives$ = this.adviceService.getObjectives();
  public readonly objectiveOptions$ = this.allObjectives$.pipe(
    take(1),
    map((objectives) =>
      objectives
        .filter((objective) => objective.display_name !== undefined)
        .map((o): SelectOption => ({ label: o.display_name!, value: o.id }))
    )
  );

  private allTrees$ = this.treeService.getAllTreeInfo();
  public readonly treeOptions$ = this.allTrees$.pipe(
    take(1),
    map((trees) =>
      trees
        .filter((tree) => tree.display_name !== undefined)
        .map((t): SelectOption => ({ label: t.display_name!, value: t.id }))
    )
  );

  public resolvedTrees$ = this.profileTrees$.pipe(
    combineLatestWith(
      this.allTrees$,
      this.allObjectives$,
      this.adviceService.getStages()
    ),
    map(([profileTrees, allTrees, objectives, stages]) =>
      profileTrees.map((profileTree) => {
        const tree = allTrees.find((t) => t.id === profileTree.treeReference);
        const objective = objectives.find(
          (o) => o.id === profileTree.objective
        );
        console.log(allTrees);
        return {
          tree,
          objective,
        };
      })
    )
  );
  constructor(
    private fb: NonNullableFormBuilder,
    private userService: UserService,
    private treeService: TreeInfoService,
    private adviceService: AdviceService,
    private toastingService: ToastingService
  ) {}

  onSubmit() {
    const selectedTree = this.form.get('tree')?.value;
    const selectedObjective = this.form.get('objective')?.value;

    if (selectedTree && selectedObjective) {
      this.userService
        .addTreeToCurrentUserProfile(selectedTree, selectedObjective)
        .subscribe(() => {
          this.form.reset();
          this.toastingService.provideSuccess(
            'You added a new tree to your profile!'
          );
          this.userService.requestRefresh();
        });
    }
  }

}
