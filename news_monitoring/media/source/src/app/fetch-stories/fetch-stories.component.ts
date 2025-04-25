import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import { Source } from '../interface';
import { SourceService } from '../http_service/source.service';


@Component({
  selector: 'app-fetch-stories',
  standalone: false,
  templateUrl: './fetch-stories.component.html',
  styleUrl: './fetch-stories.component.css'
})
export class FetchStoriesComponent {
  @Input() source?: Source;
  @Output() refreshSources = new EventEmitter<void>();

  stories: any[] = [];
  loading: boolean = false;
  fetchComplete: boolean = false;

  constructor(
    public activeModal: NgbActiveModal,
    private sourceService: SourceService,
    private toastr: ToastrService
  ) {}

  fetchStories(){
    if (!this.source) return;
    this.loading = true;
    this.sourceService.fetchStories(this.source.id).subscribe({
      next: (response) => {
        this.loading = false;
        this.fetchComplete = true;
        if (response && response.stories && response.stories.length > 0) {
          this.stories = response.stories;
          this.toastr.success(`${response.stories.length} stories fetched`, 'Success');
        } else {
          this.toastr.info('No new stories were found', 'Information');
        }
      },
      error: (error) => {
        this.loading = false;
        console.error('Error fetching stories:', error);
        this.toastr.error('Failed to fetch stories', 'Error');
      }
    });
  }
}
