import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { UserService } from 'src/app/Services/user.service';
import { Profile } from 'swagger-client';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent {
  public userProfile$: Observable<Profile | undefined> =
    this.userService.getCurrentUserProfile();

  constructor(private userService: UserService) {}
}
