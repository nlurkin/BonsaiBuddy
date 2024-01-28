import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { UserService } from './Services/user.service';
import { AuthenticationService } from './Services/authentication.service';

export const hasPermissionsGuard: CanActivateFn = (route, state) => {
  return inject(UserService).currentHasPermissions(route.data['permissions']);
};

export const isLoggedInGuard: CanActivateFn = (route, state) => {
  return inject(AuthenticationService).isUserLoggedIn();
};
