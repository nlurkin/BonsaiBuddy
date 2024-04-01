import {
  Component,
  ElementRef,
  HostListener,
  Input,
  OnDestroy,
  OnInit,
} from '@angular/core';
import * as _ from 'lodash';
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
import { SelectOption } from '../../Generic/custom-input/custom-input.component';

type LabelEvent = {
  month: number;
  label: string;
};

export type PeriodEvent = {
  startMonth: number;
  endMonth: number;
  eventId: string;
  text: string;
  category: string;
  objective: string;
  colour?: string;
  height?: number;
};

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit, OnDestroy {
  @Input() public events$!: Observable<PeriodEvent[]>;

  @HostListener('window:resize', ['$event'])
  onResize(event: Event) {
    this.refresh$.next();
  }

  @HostListener('window:scroll', ['$event'])
  onScroll(event: Event) {
    this.refresh$.next();
  }

  public months: LabelEvent[] = range(1, 12).map((month) => {
    return {
      month: month,
      label: getLocaleMonth(month, 'en', 'short'),
    } as LabelEvent;
  });

  private filteredEvents$!: Observable<PeriodEvent[]>;
  public eventsWithColourAndHeight$!: Observable<PeriodEvent[]>;
  private mutationObserver?: MutationObserver;
  private refresh$ = new BehaviorSubject<void>(undefined);
  private destroy$ = new Subject<void>();
  public readonly maxHeight$ = new BehaviorSubject<number>(0);
  public categoryFilterOptions$ = new Observable<SelectOption[]>();
  public objectiveFilterOptions$ = new Observable<SelectOption[]>();
  private selectedCategory$ = new BehaviorSubject<string | null>(null);
  private selectedObjective$ = new BehaviorSubject<string | null>(null);

  constructor(private elementRef: ElementRef) {}

  private isOverlapping(event1: PeriodEvent, event2: PeriodEvent): boolean {
    return (
      (event1.startMonth >= event2.startMonth &&
        event1.startMonth <= event2.endMonth) ||
      (event1.endMonth >= event2.startMonth &&
        event1.endMonth <= event2.endMonth)
    );
  }
  private assignBlockHeight(events: PeriodEvent[]): PeriodEvent[] {
    const baseHeight: number = 200;
    const addHeight: number = 100;

    return events.map((event) => {
      const overlappingEventsMaxHeight = events
        .filter((otherEvent) => this.isOverlapping(event, otherEvent))
        .map((event) => event.height ?? 0)
        .reduce((a, b) => Math.max(a, b), 0);

      event.height =
        overlappingEventsMaxHeight == 0
          ? baseHeight
          : overlappingEventsMaxHeight + addHeight;
      return event;
    });
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
    this.categoryFilterOptions$ = this.events$.pipe(
      map((events) =>
        _.uniq(events.map((event) => event.category)).map((type) => ({
          value: type,
          label: type,
        }))
      )
    );
    this.objectiveFilterOptions$ = this.events$.pipe(
      map((events) =>
        _.uniq(events.map((event) => event.objective)).map((type) => ({
          value: type,
          label: type,
        }))
      )
    );
    this.filteredEvents$ = combineLatest([
      this.events$,
      this.selectedCategory$,
      this.selectedObjective$,
    ]).pipe(
      map(([events, selectedCategory, selectedObjective]) =>
        events
          .filter(
            (event) =>
              selectedCategory == null || event.category == selectedCategory
          )
          .filter(
            (event) =>
              selectedObjective == null || event.objective == selectedObjective
          )
      )
    );
    this.eventsWithColourAndHeight$ = this.filteredEvents$.pipe(
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

  categoryFilterSelect(event: { originalEvent: Event; value: string }) {
    this.selectedCategory$.next(event.value);
  }
  objectiveFilterSelect(event: { originalEvent: Event; value: string }) {
    this.selectedObjective$.next(event.value);
  }
}
