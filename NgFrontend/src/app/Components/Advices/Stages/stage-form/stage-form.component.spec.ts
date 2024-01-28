import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StageFormComponent } from './stage-form.component';

describe('StageFormComponent', () => {
  let component: StageFormComponent;
  let fixture: ComponentFixture<StageFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StageFormComponent]
    });
    fixture = TestBed.createComponent(StageFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
