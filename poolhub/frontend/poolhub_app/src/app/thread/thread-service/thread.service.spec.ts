import { TestBed, inject } from '@angular/core/testing';

import { ThreadService } from './thread.service';

describe('ThreadService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ThreadService]
    });
  });

  it('should ...', inject([ThreadService], (service: ThreadService) => {
    expect(service).toBeTruthy();
  }));
});
