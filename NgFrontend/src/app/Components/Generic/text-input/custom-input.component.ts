import { Component, Input } from '@angular/core';
import { FormControl, FormGroupDirective, Validators } from '@angular/forms';

export enum InputType {
  TEXT = 'text',
  NUMBER = 'number',
  SELECT = 'select',
}

export type SelectOption = { label: string; value: string };

@Component({
  selector: 'app-custom-input',
  templateUrl: './custom-input.component.html',
  styleUrls: ['./custom-input.component.scss'],
})
export class CustomInputComponent {
  @Input() formName!: string;
  @Input() placeholder!: string;
  @Input() type: InputType = InputType.TEXT;
  @Input() options: SelectOption[] = [];

  control!: FormControl;

  constructor(private rootFormGroup: FormGroupDirective) {}

  ngOnInit() {
    this.control = this.rootFormGroup.control?.get(
      this.formName
    ) as FormControl;
  }

  public validityCheck(): string {
    if (this.control?.invalid && (this.control.dirty || this.control.touched))
      return 'invalid';
    else return '';
  }

  public isRequired(): boolean {
    return this.control?.hasValidator(Validators.required) ?? false;
  }
}
