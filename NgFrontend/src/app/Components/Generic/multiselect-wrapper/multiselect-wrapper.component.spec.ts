import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MultiselectWrapperComponent } from './multiselect-wrapper.component';

describe('MultiselectWrapperComponent', () => {
  let component: MultiselectWrapperComponent;
  let fixture: ComponentFixture<MultiselectWrapperComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MultiselectWrapperComponent]
    });
    fixture = TestBed.createComponent(MultiselectWrapperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
