import { Component } from '@angular/core';
import { Observable, map } from 'rxjs';
import { AuthenticationService } from 'src/app/Services/authentication.service';

interface MenuItem {
  label: string;
  routerLink?: string;
  action?: () => void;
  requireLogin: boolean;
  requireRole?: [];
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

  constructor(private authService: AuthenticationService) {}

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
    // {
    //   label: 'Profile',
    //   routerLink: '/profile',
    //   requireLogin: true,
    // },
    // {
    //   label: 'My Trees',
    //   routerLink: '/mytrees',
    //   requireLogin: true,
    // },
    // {
    //   label: 'Admin',
    //   routerLink: '/admin',
    //   requireLogin: true,
    //   requireRole: ['CanChangeContent'],
    // },
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

  public accessibleMenuItems$: Observable<MenuItem[]> = this.authService
    .isUserLoggedIn()
    .pipe(
      map((isLoggedIn) =>
        this.menuItems.filter((item) => {
          if (item.label === 'Login' && isLoggedIn) return false;
          return !item.requireLogin || isLoggedIn;
        })
      )
    );

  private logout() {
    console.log('logout', this.authService);
    this.authService.logOut();
  }
}
