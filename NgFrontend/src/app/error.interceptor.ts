import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable, catchError, of, throwError } from 'rxjs';
import { ToastingService } from './Services/toasting.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private toastingService: ToastingService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((error) => {
        if (error.status === 401) {
          // Do not intercept authentication errors here. Leave it to JWT
        } else {
          const description = this.extractStandardError(error.error);
          this.toastingService.provideError({
            code: error.status,
            description: description ?? 'Unknown error',
          });
        }
        return throwError(() => error); // Forward error to the next interceptor
      })
    );
  }

  private extractStandardError(error: any): string | null {
    const errorClass = Object.values(error)[0] as Object;
    const maybeDescription = Object.entries(errorClass)
      .map(([key, value]: [string, any]) =>
        key === 'description' ? value : null
      )
      .filter((x) => x !== null);
    return maybeDescription.length > 0 ? maybeDescription[0] : null;
  }
}
