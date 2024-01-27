import { Component, OnDestroy, OnInit } from '@angular/core';
import { Observable, Subject, filter, map, takeUntil } from 'rxjs';
import { MessageService } from 'primeng/api';
import { ErrorService } from './Services/error.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit, OnDestroy {
  destroy$ = new Subject<void>();

  constructor(
    private messageService: MessageService,
    private errorService: ErrorService
  ) {}

  ngOnInit(): void {
    this.errorService
      .getLastError()
      .pipe(takeUntil(this.destroy$))
      .subscribe((error) => {
        this.messageService.add({
          severity: 'error',
          summary: `Error ${error.code}`,
          detail: error.description,
          key: 'app-message',
        });
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
