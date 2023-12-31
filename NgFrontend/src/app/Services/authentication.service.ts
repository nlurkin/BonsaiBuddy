import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, map, take } from 'rxjs';
import { TokenAPI, TokenObtainPairResponse } from 'swagger-client';

export interface UserCredentials {
  username: string;
  password: string;
}

export interface LoggedInUser {
  token: string;
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

  setLoggedInUser(
    user: UserCredentials,
    responseToken: TokenObtainPairResponse
  ): void {
    const userData: LoggedInUser = {
      token: responseToken.access,
      username: user.username,
    };
    if (localStorage.getItem('userData') !== JSON.stringify(userData)) {
      localStorage.setItem('userData', JSON.stringify(userData));
    }
    this.loggedInUser.next(userData);
  }

  userValue() {
    return this.loggedInUser.value;
  }

  getLoggedInUser() {
    return this.loggedInUser;
  }

  isUserLoggedIn(): Observable<boolean> {
    return this.loggedInUser.pipe(map((user) => user !== undefined));
  }

  logIn(user: UserCredentials) {
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

  logOut() {
    localStorage.removeItem('userData');
    this.loggedInUser.next(undefined);
  }
}
