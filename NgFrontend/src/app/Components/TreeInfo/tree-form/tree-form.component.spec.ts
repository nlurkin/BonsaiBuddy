import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TreeFormComponent } from './tree-form.component';

describe('TreeFormComponent', () => {
  let component: TreeFormComponent;
  let fixture: ComponentFixture<TreeFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TreeFormComponent]
    });
    fixture = TestBed.createComponent(TreeFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
