import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { UserService } from 'src/app/Services/user.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
})
export class AdminComponent {
  public canEditAdvice$: Observable<boolean> =
    this.userService.currentUserHasPermissions('BonsaiAdvice.change_content');

  constructor(private userService: UserService) {}
}
