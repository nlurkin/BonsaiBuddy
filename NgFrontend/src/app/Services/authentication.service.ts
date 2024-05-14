import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map, of, switchMap, take } from 'rxjs';
import { TokenAPI, TokenObtainPairResponse } from 'swagger-client';

export interface UserCredentials {
  username: string;
  password: string;
}

export interface LoggedInUser {
  token: string;
  refreshToken: string;
  username: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private loggedInUser = new BehaviorSubject<LoggedInUser | undefined>(
    undefined
  );
  constructor(private auth: TokenAPI) {
    const userData = localStorage.getItem('userData');
    this.loggedInUser.next(userData ? JSON.parse(userData) : undefined);
  }

  private saveUserData(userData: LoggedInUser): void {
    if (localStorage.getItem('userData') !== JSON.stringify(userData)) {
      localStorage.setItem('userData', JSON.stringify(userData));
    }
    this.loggedInUser.next(userData);
  }

  private setLoggedInUser(
    user: UserCredentials,
    responseToken: TokenObtainPairResponse
  ): void {
    this.saveUserData({
      token: responseToken.access,
      refreshToken: responseToken.refresh,
      username: user.username,
    });
  }

  public userValue() {
    return this.loggedInUser.value;
  }

  public getLoggedInUser() {
    return this.loggedInUser;
  }

  public isUserLoggedIn(): Observable<boolean> {
    return this.loggedInUser.pipe(map((user) => user !== undefined));
  }

  public logIn(user: UserCredentials) {
    this.auth
      .tokenCreate({
        username: user.username,
        password: user.password,
        access: '',
        refresh: '',
      })
      .pipe(take(1))
      .subscribe((response) => this.setLoggedInUser(user, response));
  }

  public logOut() {
    console.log('logging out');
    localStorage.removeItem('userData');
    this.loggedInUser.next(undefined);
  }

  public refreshToken(token: string): Observable<string | undefined> {
    const oldUserValue = this.userValue();
    return oldUserValue
      ? this.auth.tokenRefreshCreate({ refresh: token, access: '' }).pipe(
          take(1),
          map((response) => {
            this.saveUserData({
              ...oldUserValue,
              token: response.access,
            });
            return response.access;
          })
        )
      : of(undefined);
  }
}
