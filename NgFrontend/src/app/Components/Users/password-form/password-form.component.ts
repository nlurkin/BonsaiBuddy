import { Component } from '@angular/core';
import {
  AbstractControl,
  NonNullableFormBuilder,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Observable, catchError, map, of, take } from 'rxjs';
import { AuthenticationService } from 'src/app/Services/authentication.service';
import { ToastingService } from 'src/app/Services/toasting.service';
import { UserService } from 'src/app/Services/user.service';
import { InputType } from '../../Generic/custom-input/custom-input.component';

const passwordMismatch: ValidatorFn = (
  control: AbstractControl
): ValidationErrors | null => {
  const password1 = control.get('password1');
  const password2 = control.get('password2');

  return password1 && password2 && password1.value !== password2.value
    ? { password_mismatch: true }
    : null;
};

@Component({
  selector: 'app-password-form',
  templateUrl: './password-form.component.html',
  styleUrls: ['./password-form.component.scss'],
})
export class PasswordFormComponent {
  public InputType = InputType;

  private validatePassword(
    control: AbstractControl
  ): Observable<ValidationErrors | null> {
    return this.userService.checkPassword(control.value).pipe(
      take(1),
      map((password) =>
        password.status ? null : { django_validation: password.message }
      ),
      catchError(() => of(null))
    );
  }

  public form = this.fb.group(
    {
      password1: this.fb.control<string | undefined>(
        undefined,
        [Validators.required, Validators.minLength(8)],
        [this.validatePassword.bind(this)]
      ),
      password2: this.fb.control<string | undefined>(undefined, [
        Validators.required,
      ]),
      oldPassword: this.fb.control<string | undefined>(undefined, [
        Validators.required,
      ]),
    },
    { validators: [passwordMismatch] }
  );

  constructor(
    private fb: NonNullableFormBuilder,
    private userService: UserService,
    private authService: AuthenticationService,
    private toastingService: ToastingService
  ) {}

  onSubmit(): void {
    const username = this.authService.userValue()?.username;
    if (this.form.valid && username) {
      this.userService
        .changePassword(
          username,
          this.form.get('oldPassword')?.value ?? '',
          this.form.get('password1')?.value ?? '',
          this.form.get('password2')?.value ?? ''
        )
        .subscribe(() => {
          this.form.reset();
          this.toastingService.provideSuccess('Password changed successfully');
        });
    }
  }
}
