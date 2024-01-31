import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export type ErrorType = {
  code: number;
  description: string;
};

@Injectable({
  providedIn: 'root',
})
export class ToastingService {
  private lastError$ = new Subject<ErrorType>();
  private lastMessage$ = new Subject<string>();
  private lastSuccess$ = new Subject<string>();

  constructor() {}

  public getLastError(): Observable<ErrorType> {
    return this.lastError$.asObservable();
  }

  public provideError(error: ErrorType): void {
    this.lastError$.next(error);
  }

  public getLastMessage(): Observable<string> {
    return this.lastMessage$.asObservable();
  }

  public provideMessage(message: string): void {
    this.lastMessage$.next(message);
  }

  public getLastSuccess(): Observable<string> {
    return this.lastSuccess$.asObservable();
  }

  public provideSuccess(message: string): void {
    this.lastSuccess$.next(message);
  }
}
