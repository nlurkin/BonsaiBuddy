import { Injectable } from '@angular/core';
import { AuthenticationService } from './authentication.service';
import { Observable, map, of, switchMap } from 'rxjs';
import { PatchedProfile, Profile, User, UsersAPI } from 'swagger-client';

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
  private readonly userProfiles$ = this.user$.pipe(
    switchMap((user) =>
      user && !user.is_superuser
        ? this.userApi.usersProfileRetrieve(user.username)
        : of(undefined)
    )
  );

  public getCurrentUserAccount(): Observable<User | undefined> {
    return this.user$;
  }

  public getCurrentUserProfile(): Observable<Profile | undefined> {
    return this.userProfiles$;
  }

  public currentUserHasPermissions(permissions: string): Observable<boolean> {
    return this.user$.pipe(
      map((user) => (user ? user.permissions.includes(permissions) : false))
    );
  }

  public currentUserHasAnyOfRole(roles: string[]): Observable<boolean> {
    return this.user$.pipe(
      map((user) =>
        user ? roles.some((role) => user.groups.includes(role)) : false
      )
    );
  }

  public updateCurrentUserProfile(
    username: string,
    profile: PatchedProfile
  ): Observable<Profile> {
    return this.userApi.usersProfilePartialUpdate(username, profile);
  }

  constructor(
    private authService: AuthenticationService,
    private userApi: UsersAPI
  ) {}
}
