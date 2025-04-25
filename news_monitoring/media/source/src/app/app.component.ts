import {Component, EventEmitter, OnInit} from '@angular/core';

import { Subject } from 'rxjs';
import { debounceTime} from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

import {Source} from './interface';
import {SourceService} from './http_service/source.service';
import { AddOrUpdateComponent } from './add-or-update/add-or-update.component';
import {DeleteComponent} from './delete/delete.component';
import {FetchStoriesComponent} from './fetch-stories/fetch-stories.component';


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
        next: (response) => {
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
    const modalRef = this.modalService.open(DeleteComponent, { centered: true });
    modalRef.componentInstance.source = source;
    modalRef.componentInstance.refreshSources = new EventEmitter();
    modalRef.componentInstance.refreshSources.subscribe(() => {
      this.fetchSources();
    });
  }

  fetchStories(sourceId: number) {
    const source = this.sources.find(s => s.id === sourceId);
    if (!source) return;

    const modalRef = this.modalService.open(FetchStoriesComponent, { centered: true, size: 'lg' });
    modalRef.componentInstance.source = source;
  }
  protected readonly Math = Math;
}
