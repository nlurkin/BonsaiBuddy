import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  catchError,
  combineLatest,
  filter,
  finalize,
  map,
  switchMap,
  take,
  tap,
  throwError,
  timer,
} from 'rxjs';
import { AuthenticationService } from './Services/authentication.service';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  private isRefreshing = new BehaviorSubject<boolean>(false);

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
    const isTokenUrl = request.url.includes('api/token');
    const isApiUrl = request.url.includes('/api/');
    return combineLatest([
      this.isRefreshing,
      this.authService.getLoggedInUser(),
    ]).pipe(
      filter(([refreshing, user]) => {
        // We must block for API call to non-refresh token URLs, if a refresh is ongoing
        // In any other case, we don't block
        return !isApiUrl || !refreshing || isTokenUrl || !user;
      }),
      take(1),
      switchMap(([_, user]) => {
        const isLoggedIn = !!user;
        if (isLoggedIn && isApiUrl && !isTokenUrl) {
          request = this.updateRequestWithToken(request, user.token);
        }

        return next.handle(request).pipe(
          catchError((error) => {
            if (
              isLoggedIn &&
              isApiUrl &&
              !isTokenUrl &&
              error instanceof HttpErrorResponse &&
              error.status === 401
            ) {
              return this.handle401Error(request, next);
            }

            return throwError(() => error);
          })
        );
      })
    );
  }

  private handle401Error(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    const refreshToken = this.authService.userValue()!.refreshToken; // We made sure of that before calling the method
    return (
      !this.isRefreshing.value
        ? this.submitRefreshTokenRequest(request, refreshToken)
        : combineLatest([
            this.isRefreshing,
            this.authService.getLoggedInUser(),
          ]).pipe(
            filter(([isRefreshing, _]) => {
              return !isRefreshing;
            }),
            take(1),
            map(([_, user]) => {
              return this.updateRequestWithToken(request, user?.token ?? '');
            })
          )
    ).pipe(switchMap((request) => next.handle(request)));
  }

  private submitRefreshTokenRequest(
    request: HttpRequest<any>,
    refreshToken: string
  ): Observable<HttpRequest<any>> {
    this.isRefreshing.next(true);

    return this.authService.refreshToken(refreshToken).pipe(
      take(1),
      map((token) => {
        this.isRefreshing.next(false);

        request = this.updateRequestWithToken(request, token ?? '');

        return request;
      }),
      catchError((err) => {
        this.isRefreshing.next(false);

        this.authService.logOut();
        return throwError(() => err);
      }),
      finalize(() => {
        // Wait a bit of time to make sure that the token refresh is completed
        // before allowing any other request (we just lost all visibility on that)
        timer(150).subscribe(() => this.isRefreshing.next(false));
      })
    );
  }
}
