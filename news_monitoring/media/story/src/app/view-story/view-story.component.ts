// src/app/components/view-story/view-story.component.ts

import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';
import { StoryService, Story } from '../story.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-view-story',
  standalone: false,
  templateUrl: './view-story.component.html',
  styleUrls: ['./view-story.component.css']
})
export class ViewStoryComponent implements OnInit, OnDestroy {
  stories: Story[] = [];
  totalItems: number = 0;
  currentPage: number = 1;
  pageSize: number = 10;
  totalPages: number = 1;
  searchQuery: string = '';
  showModal = false;
  isEditMode = false;
  editingStoryId: number | null = null;
  storyForm!: FormGroup;
  companies: any[] = [];
  sourceId: number | null = null;
  private destroy$ = new Subject<void>();
  private searchSubject = new Subject<string>();

  constructor(
    private storyService: StoryService,
    private route: ActivatedRoute,
    public router: Router,
    private fb: FormBuilder,
    public toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.route.params.pipe(takeUntil(this.destroy$)).subscribe(params => {
      if (params['sourceId']) {
        this.sourceId = +params['sourceId'];
        this.loadStoriesBySource();
      } else {
        this.loadStories();
      }
    });

    this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.currentPage = 1;
      if (this.sourceId) {
        this.loadStoriesBySource();
      } else {
        this.loadStories();
      }
    });

    this.initializeForm();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  initializeForm(): void {
    this.storyForm = this.fb.group({
      title: ['', Validators.required],
      article_url: ['', [Validators.required, Validators.pattern(/https?:\/\/.*/)]],
      body_text: ['', Validators.required],
      published_date: ['', Validators.required],
      tagged_companies: [[]]
    });
  }

  loadStories(): void {
    console.log('Loading stories with query:', this.searchQuery);
    this.storyService.getStories(this.currentPage, this.searchQuery).subscribe({
      next: (data: any) => {
        console.log('Data received:', data);
        this.stories = data.results || [];
        this.totalItems = data.count || 0;
        this.totalPages = Math.ceil(this.totalItems / this.pageSize);
      },
      error: (error) => {
        console.error('Error fetching stories:', error);
      }
    });
  }

  loadStoriesBySource(): void {
    if (!this.sourceId) return;

    console.log('Loading stories for source:', this.sourceId);
    this.storyService.getStoriesBySource(this.sourceId, this.currentPage).subscribe({
      next: (data: any) => {
        console.log('Data received:', data);
        this.stories = data.results || [];
        this.totalItems = data.count || 0;
        this.totalPages = Math.ceil(this.totalItems / this.pageSize);
      },
      error: (error) => {
        console.error('Error fetching stories for source:', error);
      }
    });
  }

  onSearchChange(): void {
    this.searchSubject.next(this.searchQuery);
  }

  onPageChange(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.currentPage = page;
      if (this.sourceId) {
        this.loadStoriesBySource();
      } else {
        this.loadStories();
      }
    }
  }

  getPages(): number[] {
    const totalPages = Math.ceil(this.totalItems / this.pageSize);
    const displayPages = 5;
    const pages: number[] = [];

    let startPage = Math.max(1, this.currentPage - Math.floor(displayPages / 2));
    let endPage = Math.min(totalPages, startPage + displayPages - 1);

    if (endPage - startPage + 1 < displayPages) {
      startPage = Math.max(1, endPage - displayPages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  }

  openAddModal(): void {
    this.isEditMode = false;
    this.editingStoryId = null;
    this.storyForm.reset({
      title: '',
      article_url: '',
      body_text: '',
      published_date: '',
      tagged_companies: []
    });
    this.loadCompanies();
    this.showModal = true;
  }

  openEditModal(story: Story): void {
    this.isEditMode = true;
    this.editingStoryId = story.id;
    this.loadCompanies();

    this.storyService.getStoryById(story.id).subscribe({
      next: (storyData) => {
        this.storyForm.patchValue({
          title: storyData.title,
          article_url: storyData.article_url,
          body_text: storyData.body_text,
          published_date: storyData.published_date,
          tagged_companies: storyData.tagged_companies
        });
        this.showModal = true;
      },
      error: (error) => {
        console.error('Error loading story details:', error);
      }
    });
  }

  loadCompanies(): void {
    this.storyService.getStoryFormData(this.editingStoryId).subscribe({
      next: (data: any) => {
        this.companies = data.companies || [];
      },
      error: (error) => {
        console.error('Error loading companies:', error);
      }
    });
  }

  closeModal(): void {
    this.showModal = false;
  }

// Update to ViewStoryComponent submitForm method
// In ViewStoryComponent - update submitForm method (if you added map function there)
submitForm(): void {
  if (this.storyForm.invalid) {
    this.storyForm.markAllAsTouched();
    return;
  }

  // Create a clean copy of the form data
  const formData = { ...this.storyForm.value };

  // Ensure dates are in proper ISO format
  if (formData.published_date) {
    // Make sure date is in ISO format (YYYY-MM-DD)
    formData.published_date = new Date(formData.published_date)
      .toISOString().split('T')[0];
  }

  // Ensure tagged_companies exists and contains numbers not strings
  if (formData.tagged_companies && Array.isArray(formData.tagged_companies)) {
    formData.tagged_companies = formData.tagged_companies.map((id: string | number) =>
      typeof id === 'string' ? parseInt(id, 10) : id
    );
  } else {
    formData.tagged_companies = [];
  }

  // For debugging - log the data before sending
  console.log('Form data to be sent:', formData);


  if (this.isEditMode && this.editingStoryId) {
    this.storyService.updateStory(this.editingStoryId, formData).subscribe({
      next: (response) => {
        // console.log('Story updated successfully:', response);
         this.toastr.success(
          `Story Updated successfully`,
          'Success'
        );
        this.closeModal();
        if (this.sourceId) {
          this.loadStoriesBySource();
        } else {
          this.loadStories();
        }
      },
      error: (error) => {
        console.error('Error updating story:', error);
        // Display error details for debugging
        if (error.error) {
          console.error('Server error details:', error.error);
          // Show user-friendly message with specifics
          let errorMessage = 'Error updating story. Please check your input and try again.';
          if (typeof error.error === 'object') {
            const errorKeys = Object.keys(error.error);
            if (errorKeys.length > 0) {
              errorMessage += ' Issues with: ' + errorKeys.join(', ');
            }
          }
          alert(errorMessage);
        }
      }
    });
  } else {
    // Add source ID if available
    if (this.sourceId) {
      formData.source = this.sourceId;
    }

    this.storyService.createStory(formData).subscribe({
      next: (response) => {
        console.log('Story created successfully:', response);
        this.toastr.success(
          `Story created successfully`,
          'Success'
        );
        this.closeModal();
        if (this.sourceId) {
          this.loadStoriesBySource();
        } else {
          this.loadStories();
        }
      },
      error: (error) => {
        console.error('Error creating story:', error);
        // Display error details for debugging
        if (error.error) {
          console.error('Server error details:', error.error);
          // Show user-friendly message with specifics
          let errorMessage = 'Error creating story. Please check your input and try again.';
          if (typeof error.error === 'object') {
            const errorKeys = Object.keys(error.error);
            if (errorKeys.length > 0) {
              errorMessage += ' Issues with: ' + errorKeys.join(', ');
            }
          }
          alert(errorMessage);
        }
      }
    });
  }
}

  deleteStory(storyId: number): void {
    if (confirm('Are you sure you want to delete this story?')) {
      this.storyService.deleteStory(storyId).subscribe({
        next: () => {
          if (this.sourceId) {
            this.loadStoriesBySource();
            this.toastr.success('Story deleted successfully', 'Success');
          } else {
            this.loadStories();
          }
        },
        error: (error) => {
          console.error('Error deleting story:', error);
            this.toastr.error('Could not delete Story', 'Error');
        }
      });
    }
  }


  get Math() {
    return Math;
  }
}
