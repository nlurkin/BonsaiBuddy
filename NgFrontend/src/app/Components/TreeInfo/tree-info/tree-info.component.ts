import { Component } from '@angular/core';
import * as _ from 'lodash';
import { map } from 'rxjs';
import { TreeInfoService } from 'src/app/Services/tree-info.service';

@Component({
  selector: 'app-tree-info',
  templateUrl: './tree-info.component.html',
  styleUrls: ['./tree-info.component.scss'],
})
export class TreeInfoComponent {
  constructor(private treeInfoService: TreeInfoService) {}

  public treeInfos$ = this.treeInfoService
    .getAllTreeInfo()
    .pipe(
      map((treeInfos) => _.sortBy(treeInfos, (v) => _.deburr(v.display_name)))
    );
}
