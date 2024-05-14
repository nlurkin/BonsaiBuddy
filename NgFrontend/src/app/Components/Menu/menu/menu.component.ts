import { Component } from '@angular/core';
import { Observable, combineLatest, map } from 'rxjs';
import { AuthenticationService } from 'src/app/Services/authentication.service';
import { UserService } from 'src/app/Services/user.service';

interface MenuItem {
  label: string;
  routerLink?: string;
  action?: () => void;
  requireLogin: boolean;
  requireRole?: string[];
}

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
})
export class MenuComponent {
  public sidebarVisible = false;
  public userName$ = this.authService
    .getLoggedInUser()
    .pipe(map((user) => user?.username));

  constructor(
    private authService: AuthenticationService,
    private userService: UserService
  ) {}

  private menuItems: MenuItem[] = [
    {
      label: 'Home',
      routerLink: '/',
      requireLogin: false,
    },
    {
      label: 'Trees',
      routerLink: '/treeinfo',
      requireLogin: false,
    },
    {
      label: 'Advices',
      routerLink: '/advices',
      requireLogin: false,
    },
    {
      label: 'Profile',
      routerLink: '/profile',
      requireLogin: true,
    },
    {
      label: 'My Trees',
      routerLink: '/profile/mytrees',
      requireLogin: true,
    },
    {
      label: 'Admin',
      routerLink: '/admin',
      requireLogin: true,
      requireRole: ['content_manager'],
    },
    {
      label: 'Login',
      routerLink: '/login',
      requireLogin: false,
    },
    {
      label: 'Logout',
      action: this.logout.bind(this),
      requireLogin: true,
    },
  ];

  public accessibleMenuItems$: Observable<MenuItem[]> = combineLatest([
    this.authService.isUserLoggedIn(),
    this.userService.getCurrentUserAccount(),
  ]).pipe(
    map(([isLoggedIn, userAccount]) =>
      this.menuItems.filter((item) => {
        if (item.label === 'Login' && isLoggedIn) return false;
        const loginOk = !item.requireLogin || isLoggedIn;
        const roleOk =
          !item.requireRole ||
          item.requireRole.some((role) => userAccount?.groups.includes(role));
        return loginOk && roleOk;
      })
    )
  );

  private logout() {
    this.authService.logOut();
  }
}
