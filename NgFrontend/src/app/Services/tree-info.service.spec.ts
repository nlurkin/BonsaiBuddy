import { TestBed } from '@angular/core/testing';

import { TreeInfoService } from './tree-info.service';

describe('TreeInfoServiceService', () => {
  let service: TreeInfoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TreeInfoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
