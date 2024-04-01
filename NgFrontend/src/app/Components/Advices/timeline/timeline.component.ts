import {
  Component,
  ElementRef,
  HostListener,
  Input,
  OnInit,
} from '@angular/core';
import { range } from 'lodash';
import {
  BehaviorSubject,
  Observable,
  Subject,
  combineLatest,
  map,
  takeUntil,
} from 'rxjs';
import { getLocaleMonth } from 'src/app/utils';

type LabelEvent = {
  month: number;
  label: string;
};

export type PeriodEvent = {
  startMonth: number;
  endMonth: number;
  eventId: string;
  colour?: string;
  height?: number;
};

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit {
  @Input() public events$!: Observable<PeriodEvent[]>;

  @HostListener('window:resize', ['$event'])
  onResize(event: Event) {
    this.refresh$.next();
  }

  public months: LabelEvent[] = range(1, 12).map((month) => {
    return {
      month: month,
      label: getLocaleMonth(month, 'en', 'short'),
    } as LabelEvent;
  });

  public eventsWithColourAndHeight$!: Observable<PeriodEvent[]>;
  private mutationObserver?: MutationObserver;
  private refresh$ = new BehaviorSubject<void>(undefined);
  private destroy$ = new Subject<void>();
  public readonly maxHeight$ = new BehaviorSubject<number>(0);

  constructor(private elementRef: ElementRef) {}

  private isOverlapping(event1: PeriodEvent, event2: PeriodEvent): boolean {
    return (
      (event1.startMonth >= event2.startMonth &&
        event1.startMonth <= event2.endMonth) ||
      (event1.endMonth >= event2.startMonth &&
        event1.endMonth <= event2.endMonth)
    );
  }
  private blockHeight(
    thisEvent: PeriodEvent,
    allEvents: PeriodEvent[]
  ): number {
    const otherEvents = allEvents.filter((event) => event !== thisEvent);
    const baseHeight = 200;
    const addHeight = 100;
    // Compute the number of events that are overlapping fully or partially with this one
    const containedEvents = otherEvents.filter((event) =>
      this.isOverlapping(thisEvent, event)
    );

    return baseHeight + containedEvents.length * addHeight;
  }

  public assignColours(
    colours: string[],
    events: PeriodEvent[]
  ): PeriodEvent[] {
    let colourIndex = 0;
    const colouredEvents = events.map((event) => {
      const overlappingEvents = events.filter((otherEvent) =>
        this.isOverlapping(event, otherEvent)
      );
      const overlappingColours = overlappingEvents.map((event) => event.colour);
      const availableColours = colours.filter(
        (colour) => !overlappingColours.includes(colour)
      );
      const colour = availableColours[colourIndex];
      colourIndex = (colourIndex + 1) % colours.length;
      return { ...event, colour };
    });
    return colouredEvents;
  }

  private positionPeriodBlock(thisEvent: PeriodEvent): void {
    // Get the element to position
    const periodBlock = document.getElementById(thisEvent.eventId);

    // Get the elements to position relative to
    const startElement = document.getElementById(
      'label-' + thisEvent.startMonth
    );
    const endElement = document.getElementById('label-' + thisEvent.endMonth);

    if (!periodBlock || !startElement || !endElement) return;
    // Get the position of the relative element
    const positionStart = startElement.getBoundingClientRect();
    const positionEnd = endElement.getBoundingClientRect();
    const scrollPosition = window.scrollY;
    const blockHeight = thisEvent.height ?? 200;

    // Set the position of the period block
    const blockWidth = positionEnd.right - positionStart.left + 40;
    periodBlock.style.top =
      positionStart.top + scrollPosition - blockHeight / 2 - 20 + 'px';
    periodBlock.style.left = positionStart.left - 20 + 'px';
    periodBlock.style.width = blockWidth + 'px';
    periodBlock.style.height = blockHeight + 'px';
  }

  private placeBlocks(events: PeriodEvent[]): void {
    events.forEach((event, index) => {
      this.positionPeriodBlock(event);
    });
  }

  ngOnInit() {
    this.eventsWithColourAndHeight$ = this.events$.pipe(
      map((events) =>
        this.assignColours(
          range(1, 10).map((i) => 'colour' + i),
          events
        )
      ),
      map((events) => this.assignBlockHeight(events))
    );
    combineLatest([this.eventsWithColourAndHeight$, this.refresh$])
      .pipe(takeUntil(this.destroy$))
      .subscribe(([events]) => {
        this.maxHeight$.next(
          events.reduce((acc, event) => {
            return Math.max(acc, event.height ?? 0);
          }, 0)
        );
        this.placeBlocks(events);
      });

    this.mutationObserver = new MutationObserver((mutations) => {
      this.refresh$.next();
    });

    this.mutationObserver.observe(this.elementRef.nativeElement.parentNode, {
      attributes: true,
      childList: true,
      subtree: true,
    });
  }

  ngOnDestroy() {
    if (this.mutationObserver) {
      this.mutationObserver.disconnect();
    }
    this.destroy$.next();
    this.destroy$.complete();
  }
}
