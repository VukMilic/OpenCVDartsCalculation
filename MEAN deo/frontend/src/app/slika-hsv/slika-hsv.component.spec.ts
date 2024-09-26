import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SlikaHsvComponent } from './slika-hsv.component';

describe('SlikaHsvComponent', () => {
  let component: SlikaHsvComponent;
  let fixture: ComponentFixture<SlikaHsvComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SlikaHsvComponent]
    });
    fixture = TestBed.createComponent(SlikaHsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
