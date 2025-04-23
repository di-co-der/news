import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewSourcesComponent } from './view-sources.component';

describe('ViewSourcesComponent', () => {
  let component: ViewSourcesComponent;
  let fixture: ComponentFixture<ViewSourcesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ViewSourcesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewSourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
