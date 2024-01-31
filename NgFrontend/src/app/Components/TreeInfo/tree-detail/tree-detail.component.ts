import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { map, switchMap } from 'rxjs';
import { TreeInfoService } from 'src/app/Services/tree-info.service';
import { filterNullish } from 'src/app/rxjs-util';

@Component({
  selector: 'app-tree-detail',
  templateUrl: './tree-detail.component.html',
  styleUrls: ['./tree-detail.component.scss'],
})
export class TreeDetailComponent {
  public tree$ = this.route.paramMap.pipe(
    map((params) => params.get('id')),
    filterNullish(),
    switchMap((id) => this.treeService.getTreeInfo(id))
  );

  constructor(
    public route: ActivatedRoute,
    public treeService: TreeInfoService
  ) {}
}
