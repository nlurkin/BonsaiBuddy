import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TreeInfo, TreesAPI } from 'swagger-client';

@Injectable({
  providedIn: 'root',
})
export class TreeInfoService {
  constructor(private treeInfoService: TreesAPI) {}

  getAllTreeInfo(): Observable<TreeInfo[]> {
    return this.treeInfoService.treesList();
  }

  getTreeInfo(id: string): Observable<TreeInfo> {
    return this.treeInfoService.treesRetrieve(id);
  }
}
