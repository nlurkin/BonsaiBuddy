import { Injectable } from '@angular/core';
import { AuthenticationService } from './authentication.service';
import { Observable, map, of, switchMap } from 'rxjs';
import { User, UsersAPI } from 'swagger-client';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private readonly user$ = this.authService
    .getLoggedInUser()
    .pipe(
      switchMap((user) =>
        user ? this.userApi.usersRetrieve(user.username) : of(undefined)
      )
    );

  public getCurrentUserProfile(): Observable<User | undefined> {
    return this.user$;
  }

  public currentHasPermissions(permissions: string): Observable<boolean> {
    return this.user$.pipe(
      map((user) => (user ? user.permissions.includes(permissions) : false))
    );
  }

  constructor(
    private authService: AuthenticationService,
    private userApi: UsersAPI
  ) {}
}
