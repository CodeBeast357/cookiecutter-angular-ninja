import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManagedAccountComponent } from './managed-account.component';

describe('ManagedAccountComponent', () => {
  let component: ManagedAccountComponent;
  let fixture: ComponentFixture<ManagedAccountComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ManagedAccountComponent]
    });
    fixture = TestBed.createComponent(ManagedAccountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
