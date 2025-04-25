import {Component, EventEmitter, OnInit} from '@angular/core';

import { Subject } from 'rxjs';
import { debounceTime} from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

import {Source, SourceResponse} from './interface';
import {SourceService} from './http_service/source.service';
import { AddOrUpdateComponent } from './add-or-update/add-or-update.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  private searchSubject = new Subject<string>();

  sources: Source[] = [];

  totalItems: number = 0;
  currentPage: number = 1;
  pageSize: number = 10;
  next: string | null = null;
  previous: string | null = null;

  searchQuery: string = '';

  constructor(
    private sourceService: SourceService,
    private modalService: NgbModal,
    private toastr: ToastrService
  ) {}

  ngOnInit(){
    this.fetchSources();
    this.searchSubject.pipe(
      debounceTime(300)
    ).subscribe(() => {
      this.currentPage = 1;
      this.fetchSources();
    });
  }

  fetchSources(){
    this.sourceService.search(this.currentPage, this.searchQuery)
      .subscribe({
        next: (response: SourceResponse) => {
          this.sources = response.results;
          this.totalItems = response.count;
          this.next = response.next;
          this.previous = response.previous;
        },
        error: (error) => {
          console.error('Error fetching sources:', error);
          this.toastr.error('Failed to load sources', 'Error');
        }
      });
  }

  onSearchChange() {
    this.searchSubject.next(this.searchQuery);
  }

  onPageChange(page: number){
    if (page >= 1 && page <= Math.ceil(this.totalItems / this.pageSize) && page !== this.currentPage) {
      this.currentPage = page;
      this.fetchSources();
    }
  }

  add() {
    const modalRef = this.modalService.open(AddOrUpdateComponent, { centered: true });
    modalRef.componentInstance.refreshSources = new EventEmitter<void>();
    modalRef.componentInstance.refreshSources.subscribe(() => {
      this.fetchSources();
    });
  }

   edit(source: Source) {
      const modalRef = this.modalService.open(AddOrUpdateComponent, { centered: true });
      modalRef.componentInstance.source = source;
      modalRef.componentInstance.refreshSources = new EventEmitter<void>();
      modalRef.componentInstance.refreshSources.subscribe(() => {
        this.fetchSources();
      });
    }

  delete(source: Source){
    if (confirm('Are you sure you want to delete this source?')) {
      this.sourceService.delete(source.id).subscribe({
        next: () => {
          this.toastr.success('Source deleted successfully', 'Success');
          this.fetchSources();
        },
        error: (error) => {
          console.error('Error deleting source:', error);
          this.toastr.error('Failed to delete source', 'Error');
        }
      });
    }
  }

  // Fetch stories from a source
  fetchStories(sourceId: number) {
    this.sourceService.fetchStories(sourceId).subscribe({
      next: (response) => {
        if (response && response.stories && response.stories.length > 0) {
          this.toastr.success(`${response.stories.length} stories fetched`, 'Success');
          // Show stories in modal or navigate to stories view
          // this.router.navigate(['/sources/stories', sourceId]);
        } else {
          this.toastr.info('No new stories were found', 'Information');
        }
      },
      error: (error) => {
        console.error('Error fetching stories:', error);
        this.toastr.error('Failed to fetch stories', 'Error');
      }
    });
  }
  protected readonly Math = Math;
}
