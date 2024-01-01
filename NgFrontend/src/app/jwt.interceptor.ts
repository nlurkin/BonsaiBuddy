import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, of, switchMap, throwError } from 'rxjs';
import { AuthenticationService } from './Services/authentication.service';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  private isRefreshing = false;

  constructor(private authService: AuthenticationService) {}

  private updateRequestWithToken(request: HttpRequest<any>, token: string) {
    return request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    const user = this.authService.userValue();
    const isLoggedIn = !!user;
    const isApiUrl = request.url.includes('/api/');
    if (isLoggedIn && isApiUrl) {
      request = this.updateRequestWithToken(request, user.token);
    }

    return next.handle(request).pipe(
      catchError((error) => {
        if (
          isLoggedIn &&
          error instanceof HttpErrorResponse &&
          !request.url.includes('api/token') &&
          error.status === 401
        ) {
          return this.handle401Error(request, next);
        }

        return throwError(() => error);
      })
    );
  }

  private handle401Error(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    const user = this.authService.userValue()!; // We made sure of that before calling the method
    return (
      !this.isRefreshing
        ? this.submitRefreshTokenRequest(request, user.refreshToken)
        : of(this.updateRequestWithToken(request, user.refreshToken))
    ).pipe(switchMap((request) => next.handle(request)));
  }

  private submitRefreshTokenRequest(
    request: HttpRequest<any>,
    refreshToken: string
  ): Observable<HttpRequest<any>> {
    this.isRefreshing = true;

    return this.authService.refreshToken(refreshToken).pipe(
      switchMap((token) => {
        this.isRefreshing = false;

        request = this.updateRequestWithToken(request, token ?? '');

        return of(request);
      }),
      catchError((err) => {
        this.isRefreshing = false;

        this.authService.logOut();
        return throwError(() => err);
      })
    );
  }
}
