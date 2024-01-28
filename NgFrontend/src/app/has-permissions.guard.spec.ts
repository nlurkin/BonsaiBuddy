import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { hasPermissionsGuard } from './has-permissions.guard';

describe('hasPermissionsGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => hasPermissionsGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
