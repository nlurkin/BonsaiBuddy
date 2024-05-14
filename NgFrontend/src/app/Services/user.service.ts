import { Injectable } from '@angular/core';
import { AuthenticationService } from './authentication.service';
import {
  BehaviorSubject,
  Observable,
  combineLatest,
  map,
  of,
  switchMap,
  take,
} from 'rxjs';
import {
  ChangePassword,
  PasswordCheckResponse,
  PatchedProfile,
  Profile,
  User,
  UsersAPI,
} from 'swagger-client';
import { filterDefined } from '../rxjs-util';
import { bsonIdNull } from '../constants';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private refresh$ = new BehaviorSubject<void>(undefined);

  private readonly user$ = this.authService
    .getLoggedInUser()
    .pipe(
      switchMap((user) =>
        user ? this.userApi.usersRetrieve(user.username) : of(undefined)
      )
    );
  private readonly userProfiles$ = combineLatest([
    this.user$,
    this.refresh$,
  ]).pipe(
    switchMap(([user]) =>
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

  public updateUserProfile(
    username: string,
    profile: PatchedProfile
  ): Observable<Profile> {
    return this.userApi.usersProfilePartialUpdate(username, profile);
  }

  public updateCurrentUserProfile(
    profile: PatchedProfile
  ): Observable<Profile> {
    return this.user$.pipe(
      filterDefined(),
      take(1),
      switchMap((user) =>
        this.userApi.usersProfilePartialUpdate(user.username, profile)
      )
    );
  }

  public addTreeToCurrentUserProfile(
    treeReference: string,
    objective: string
  ): Observable<Profile> {
    return this.userProfiles$.pipe(
      filterDefined(),
      take(1),
      switchMap((user) =>
        this.userApi.usersProfilePartialUpdate(user.username, {
          my_trees: [
            ...user.my_trees,
            { oid: bsonIdNull, treeReference, objective },
          ],
        })
      )
    );
  }

  public updateTreeOfCurrentUserProfile(
    collectionId: string,
    objective: string
  ): Observable<Profile> {
    return this.userProfiles$.pipe(
      filterDefined(),
      take(1),
      switchMap((user) =>
        this.userApi.usersProfilePartialUpdate(user.username, {
          my_trees: user.my_trees.map((tree) =>
            tree.oid === collectionId ? { ...tree, objective } : tree
          ),
        })
      )
    );
  }

  public checkPassword(password: string): Observable<PasswordCheckResponse> {
    return this.userApi.userProfileCheckPasswordValidity({ password });
  }

  public changePassword(
    username: string,
    oldPassword: string,
    newPassword: string,
    newPasswordConfirm: string
  ): Observable<ChangePassword> {
    return this.userApi.usersProfilePasswordUpdate(username, {
      old_password: oldPassword,
      password: newPassword,
      password2: newPasswordConfirm,
    });
  }

  public requestRefresh() {
    this.refresh$.next(undefined);
  }

  constructor(
    private authService: AuthenticationService,
    private userApi: UsersAPI
  ) {}
}
