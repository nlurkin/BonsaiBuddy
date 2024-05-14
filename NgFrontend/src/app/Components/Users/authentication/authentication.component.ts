import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/Services/authentication.service';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.scss'],
})
export class AuthenticationComponent {
  public loginForm = this.fb.group({
    username: this.fb.control<string | undefined>(undefined, [
      Validators.required,
      Validators.maxLength(100),
    ]),
    password: this.fb.control('', [
      Validators.required,
      Validators.maxLength(100),
    ]),
  });
  constructor(
    private fb: FormBuilder,
    private authService: AuthenticationService
  ) {}

  login() {
    const loginValues = this.loginForm.getRawValue();
    if (
      this.loginForm.invalid ||
      !loginValues.username ||
      !loginValues.password
    )
      return;

    this.authService.logIn({
      username: loginValues.username,
      password: loginValues.password,
    });
  }

  logout() {
    this.authService.logOut();
  }

  public userIsLoggedIn$ = this.authService.isUserLoggedIn();
  public loggedInUser$ = this.authService.getLoggedInUser();
}
