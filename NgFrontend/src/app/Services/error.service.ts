import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export type ErrorType = {
  code: number;
  description: string;
};

@Injectable({
  providedIn: 'root',
})
export class ErrorService {
  private lastError$ = new Subject<ErrorType>();

  constructor() {}

  public getLastError(): Observable<ErrorType> {
    return this.lastError$.asObservable();
  }

  public provideError(error: ErrorType): void {
    this.lastError$.next(error);
  }
}
