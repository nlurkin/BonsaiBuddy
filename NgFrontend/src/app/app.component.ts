import { Component, OnDestroy, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { Subject, takeUntil } from 'rxjs';
import { ToastingService } from './Services/toasting.service';

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
    private toastingService: ToastingService
  ) {}

  ngOnInit(): void {
    this.toastingService
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
    this.toastingService
      .getLastSuccess()
      .pipe(takeUntil(this.destroy$))
      .subscribe((message) => {
        this.messageService.add({
          severity: 'success',
          summary: `Success`,
          detail: message,
          key: 'app-message',
        });
      });
    this.toastingService
      .getLastMessage()
      .pipe(takeUntil(this.destroy$))
      .subscribe((message) => {
        this.messageService.add({
          severity: 'info',
          summary: `Info`,
          detail: message,
          key: 'app-message',
        });
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
