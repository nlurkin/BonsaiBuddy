import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TreeDetailComponent } from './tree-detail.component';

describe('TreeDetailComponent', () => {
  let component: TreeDetailComponent;
  let fixture: ComponentFixture<TreeDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TreeDetailComponent]
    });
    fixture = TestBed.createComponent(TreeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
