import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable, catchError, of, throwError } from 'rxjs';
import { ErrorService } from './Services/error.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private errorService: ErrorService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((error) => {
        if (error.status === 401) {
          // Do not intercept authentication errors here. Leave it to JWT
        } else {
          const description = error?.error?.description
            ? error.error.description
            : 'Unknown error';
          this.errorService.provideError({ code: error.status, description });
        }
        return throwError(() => error); // Forward error to the next interceptor
      })
    );
  }
}
