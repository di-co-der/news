import { Component, EventEmitter, OnInit } from '@angular/core';

import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Story } from './interface';
import { StoryService } from './http-service/story.service';
import { AddOrUpdateComponent } from './add-or-update/add-or-update.component';
import { DeleteComponent } from './delete/delete.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  private searchSubject = new Subject<string>();

  stories: Story[] = [];

  totalItems: number = 0;
  currentPage: number = 1;
  pageSize: number = 10;
  next: string | null = null;
  previous: string | null = null;

  searchQuery: string = '';

  constructor(
    private storyService: StoryService,
    private modalService: NgbModal,
    private toastr: ToastrService
  ) {
  }

  ngOnInit() {
    this.fetchStories();
    this.searchSubject.pipe(
      debounceTime(300)
    ).subscribe(() => {
      this.currentPage = 1;
      this.fetchStories();
    });
  }

  fetchStories() {
    this.storyService.search(this.currentPage, this.searchQuery)
      .subscribe({
        next: (response) => {
          this.stories = response.results;
          this.totalItems = response.count;
          this.next = response.next;
          this.previous = response.previous;
        },
        error: (error) => {
          console.error('Error fetching stories:', error);
          this.toastr.error('Failed to load stories', 'Error');
        }
      });
  }

  onSearchChange() {
    this.searchSubject.next(this.searchQuery);
  }

  onPageChange(page: number) {
    if (page >= 1 && page <= Math.ceil(this.totalItems / this.pageSize) && page !== this.currentPage) {
      this.currentPage = page;
      this.fetchStories();
    }
  }

  add() {
    const modalRef = this.modalService.open(AddOrUpdateComponent, {centered: true});
    modalRef.componentInstance.refreshStories = new EventEmitter<void>();
    modalRef.componentInstance.refreshStories.subscribe(() => {
      this.fetchStories();
    });
  }

  edit(story: Story) {
    const modalRef = this.modalService.open(AddOrUpdateComponent, {centered: true});
    modalRef.componentInstance.story = story;
    modalRef.componentInstance.refreshStories = new EventEmitter<void>();
    modalRef.componentInstance.refreshStories.subscribe(() => {
      this.fetchStories();
    });
  }

  delete(story: Story) {
    const modalRef = this.modalService.open(DeleteComponent, {centered: true});
    console.log("after delete component")
    modalRef.componentInstance.story = story;
    modalRef.componentInstance.refreshStories = new EventEmitter();
    modalRef.componentInstance.refreshStories.subscribe(() => {
      this.fetchStories();
    });
  }

  protected readonly Math = Math;
}
