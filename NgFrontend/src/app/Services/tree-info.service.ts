import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TreeInfo, TreesAPI } from 'swagger-client';

export type BasicTreeInfo = Omit<TreeInfo, 'techniques'>;

@Injectable({
  providedIn: 'root',
})
export class TreeInfoService {
  constructor(private treeInfoService: TreesAPI) {}

  public getAllTreeInfo(): Observable<TreeInfo[]> {
    return this.treeInfoService.treesList();
  }

  public getTreeInfo(id: string): Observable<TreeInfo> {
    return this.treeInfoService.treesRetrieve(id);
  }

  public updateBasicTreeInfo(
    id: string,
    treeInfo: Partial<BasicTreeInfo>
  ): Observable<TreeInfo> {
    return this.treeInfoService.treesPartialUpdate(id, treeInfo);
  }

  public createTreeInfo(treeInfo: TreeInfo): Observable<TreeInfo> {
    return this.treeInfoService.treesCreate(treeInfo);
  }

  public deleteTreeInfo(id: string): Observable<TreeInfo> {
    return this.treeInfoService.treesDestroy(id);
  }
}
