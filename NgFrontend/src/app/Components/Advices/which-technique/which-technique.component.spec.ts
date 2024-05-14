import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhichTechniqueComponent } from './which-technique.component';

describe('WhichTechniqueComponent', () => {
  let component: WhichTechniqueComponent;
  let fixture: ComponentFixture<WhichTechniqueComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WhichTechniqueComponent]
    });
    fixture = TestBed.createComponent(WhichTechniqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
