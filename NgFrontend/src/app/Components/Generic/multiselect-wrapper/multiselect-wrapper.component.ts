import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { BehaviorSubject } from 'rxjs';
import { SelectOption } from '../custom-input/custom-input.component';

@Component({
  selector: 'app-multiselect-wrapper',
  templateUrl: './multiselect-wrapper.component.html',
  styleUrls: ['./multiselect-wrapper.component.scss'],
})
export class MultiselectWrapperComponent implements OnInit {
  @Input() control!: FormControl;
  @Input() options: SelectOption[] = [];
  @Input() id!: string;
  @Input() maxItemsToDisplay: number = 2;
  @Input() selectedItemsLabel: string = '{0} items selected';
  @Input() styleClass: string = '';

  public readonly displayMode = new BehaviorSubject<'comma' | 'chip'>('chip');

  ngOnInit(): void {
    this.control.valueChanges.subscribe((value: never[]) => {
      this.displayMode.next(
        value.length > this.maxItemsToDisplay ? 'comma' : 'chip'
      );
    });
  }
}
