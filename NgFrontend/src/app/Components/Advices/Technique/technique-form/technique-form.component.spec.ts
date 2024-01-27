import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TechniqueFormComponent } from './technique-form.component';

describe('TechniqueFormComponent', () => {
  let component: TechniqueFormComponent;
  let fixture: ComponentFixture<TechniqueFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TechniqueFormComponent]
    });
    fixture = TestBed.createComponent(TechniqueFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
