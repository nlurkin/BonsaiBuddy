import { Component } from '@angular/core';
import { NonNullableFormBuilder } from '@angular/forms';
import { take } from 'rxjs';
import { UserService } from 'src/app/Services/user.service';
import { getCountries } from 'src/app/utils';
import { PatchedProfile, Profile } from 'swagger-client';
import { InputType } from '../../Generic/text-input/custom-input.component';
import { CountryObject } from 'src/app/types';

@Component({
  selector: 'app-profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.scss'],
})
export class ProfileFormComponent {
  public InputType = InputType;
  public profileForm = this.fb.group({
    country: this.fb.control<string | undefined>(undefined),
  });

  public countryOptions = getCountries().map((country: CountryObject) => ({
    value: country.countryCode,
    label: country.countryNameEn,
  }));

  private currentProfile: Profile | undefined;

  constructor(
    private fb: NonNullableFormBuilder,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.userService
      .getCurrentUserProfile()
      .pipe(take(1))
      .subscribe((profile) => {
        this.currentProfile = profile;
        this.profileForm.patchValue({
          ...profile,
        });
      });
  }

  public onSubmit(): void {
    if (!this.profileForm.valid || !this.currentProfile) return;
    const updatedProfile = this.formToEntity();
    if (!updatedProfile) return;

    this.userService
      .updateCurrentUserProfile(this.currentProfile.username, updatedProfile)
      .pipe(take(1))
      .subscribe(() => {});
  }

  private formToEntity(): PatchedProfile | undefined {
    if (!this.currentProfile) return undefined;
    const country = this.profileForm.controls.country ?? undefined;
    return {
      ...this.profileForm.value,
    };
  }
}
