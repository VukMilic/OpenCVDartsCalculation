import { TestBed } from '@angular/core/testing';

import { SlikaHsvService } from './slika-hsv.service';

describe('SlikaHsvService', () => {
  let service: SlikaHsvService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SlikaHsvService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
