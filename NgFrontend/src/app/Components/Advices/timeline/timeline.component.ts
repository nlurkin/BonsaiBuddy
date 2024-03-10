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
import { Month } from 'src/app/types';
import { getLocaleMonth } from 'src/app/utils';

type LabelEvent = {
  month: Month;
  label: string;
};

export type PeriodEvent = {
  startMonth: Month;
  endMonth: Month;
  eventId: string;
  colour?: string;
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

  public MonthEnum = Month;
  public months: LabelEvent[] = Object.keys(Month)
    .filter((key) => !isNaN(Number(key)))
    .map((month) => {
      const monthVal = Number(month);
      return {
        month: Month[month as keyof typeof Month] as Month,
        label: getLocaleMonth(monthVal, 'en', 'short'),
      } as LabelEvent;
    });

  public eventsWithColour$!: Observable<PeriodEvent[]>;
  private mutationObserver?: MutationObserver;
  private refresh$ = new BehaviorSubject<void>(undefined);
  private destroy$ = new Subject<void>();

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

  private positionPeriodBlock(
    thisEvent: PeriodEvent,
    blockHeight: number
  ): void {
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
      this.positionPeriodBlock(
        event,
        this.blockHeight(event, events.slice(index + 1))
      );
    });
  }

  ngOnInit() {
    this.eventsWithColour$ = this.events$.pipe(
      map((events) =>
        this.assignColours(
          range(1, 10).map((i) => 'colour' + i),
          events
        )
      )
    );
    combineLatest([this.eventsWithColour$, this.refresh$])
      .pipe(takeUntil(this.destroy$))
      .subscribe(([events]) => {
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
