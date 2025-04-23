import { Component, OnDestroy, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { SourceService } from '../source.service';


interface Source {
  id: number;
  name: string;
  url: string;
  tagged_companies?: any[];
}

@Component({
  selector: 'app-view-sources',
  templateUrl: './view-sources.component.html',
  standalone: false,
  styleUrls: ['./view-sources.component.css']
})
export class ViewSourcesComponent implements OnInit, OnDestroy {
  sources: Source[] = [];
  //pagination
  totalItems: number = 0;
  currentPage: number = 1;
  pageSize: number = 10;
  totalPages: number = 1;
  searchQuery: string = '';
  showModal = false;
  showStoriesModal = false;
  importedStories: any[] = [];
  currentSource: any = null;
  isEditMode = false;
  editingSourceId: number | null = null;
  sourceForm!: FormGroup;
  companies: any[] = [];
  private searchSubject = new Subject<string>();

  constructor(
    private sourceService: SourceService,
    public router: Router,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.loadSources();
    this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(() => {
      this.currentPage = 1;
      this.loadSources();
    });
    this.initializeForm();
  }

  initializeForm(): void {
    this.sourceForm = this.fb.group({
      name: ['', Validators.required],
      url: ['', [Validators.required, Validators.pattern(/https?:\/\/.*/)]],
      tagged_companies: [[]]
    });
  }

  loadSources(): void {
    console.log('Loading sources with query:', this.searchQuery);
    this.sourceService.getSources(this.currentPage, this.searchQuery).subscribe({
      next: (data: any) => {
        console.log('Data received:', data);
        this.sources = data.results || [];
        this.totalItems = data.count || 0;
        this.totalPages = Math.ceil(this.totalItems / this.pageSize);
      },
      error: (error) => {
        console.error('Error fetching sources:', error);
      }
    });
  }

  onPageChange(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.currentPage = page;
      this.loadSources();
    }
  }

  onSearchChange(): void {
    this.searchSubject.next(this.searchQuery);
  }

  // ——— Modal handlers ———
  openAddModal() {
    this.isEditMode = false;
    this.editingSourceId = null;
    this.initializeForm();
    this.fetchCompanies();
    this.showModal = true;
    this.addModalClass();
  }

  openEditModal(src: Source) {
    this.isEditMode = true;
    this.editingSourceId = src.id;
    this.fetchSourceFormData(src.id);
    this.showModal = true;
    this.addModalClass();
  }

  closeModal() {
    this.showModal = false;
    this.removeModalClass();
    this.sourceForm.reset();
  }

  // Helper methods to manage body class for modal
  private addModalClass() {
    document.body.classList.add('modal-open');
  }

  private removeModalClass() {
    document.body.classList.remove('modal-open');
  }

  fetchCompanies(): void {
    this.sourceService.getCompanies().subscribe({
      next: (data: any) => {
        if (Array.isArray(data)) {
          this.companies = data;
        } else if (data && Array.isArray(data.results)) {
          this.companies = data.results;
        } else {
          console.error('Unexpected format for companies data:', data);
          this.companies = [];
        }
      },
      error: (error) => {
        console.error('Error fetching companies:', error);
        this.companies = [];
      }
    });
  }

fetchSourceFormData(sourceId: number): void {
  this.sourceService.getSourceFormData(sourceId).subscribe({
    next: (data: any) => {
      console.log('Form data received:', data);

      // Check if data has the expected structure
      if (!data) {
        console.error('Received empty data from API');
        return;
      }

      // Handle companies data
      if (data.companies) {
        this.companies = data.companies;
      } else {
        // If the API call doesn't return companies, fetch them separately
        this.fetchCompanies();
      }

      // Handle source data - two possible response structures
      const sourceData = data.source || data;
      if (sourceData) {
        console.log('Source data:', sourceData);

        // Get tagged companies from either format
        const taggedCompanies = data.tagged_companies ||
                               sourceData.tagged_companies ||
                               [];
        console.log('Tagged companies:', taggedCompanies);

        this.sourceForm.patchValue({
          name: sourceData.name,
          url: sourceData.url,
          tagged_companies: taggedCompanies
        });
      } else {
        console.error('Could not find source data in API response');
      }
    },
    error: (error) => {
      console.error('Error fetching source data:', error);
      // If source data fetch fails, at least try to get companies
      this.fetchCompanies();
    }
  });
}

  deleteSource(id: number) {
    if (!confirm('Are you sure you want to delete this source?')) return;
    this.sourceService.deleteSource(id).subscribe({
      next: () => this.loadSources(),
      error: (err) => {
        console.error('Delete failed', err);
        alert('Could not delete source');
      }
    });
  }

  submitForm() {
    if (this.sourceForm.invalid) return;

    const formData = this.sourceForm.value;

    // Ensure tagged_companies is always an array
    if (!formData.tagged_companies) {
      formData.tagged_companies = [];
    }

    let obs;
    if (this.isEditMode && this.editingSourceId != null) {
      obs = this.sourceService.updateSource(this.editingSourceId, formData);
    } else {
      obs = this.sourceService.createSource(formData);
    }

    obs.subscribe({
      next: () => {
        alert(`Source ${this.isEditMode ? 'updated' : 'created'} successfully`);
        this.closeModal();
        this.loadSources();
      },
      error: (err) => {
        console.error(`Error ${this.isEditMode ? 'updating' : 'creating'} source:`, err);
        alert(`Failed to ${this.isEditMode ? 'update' : 'create'} source`);
      }
    });
  }

  fetchStory(sourceId: number): void {
    this.sourceService.fetchStory(sourceId).subscribe(
      (response) => {
        this.importedStories = response.stories || [];
        this.currentSource = this.sources.find(s => s.id === sourceId);
        this.showStoriesModal = true;
      },
      (error) => {
        console.error('Error fetching stories:', error);
        alert('Error fetching stories. Please try again.');
      }
    );
  }

  closeStoriesModal(): void {
    this.showStoriesModal = false;
    this.importedStories = [];
  }

  getPages(): number[] {
    const pageCount = Math.ceil(this.totalItems / this.pageSize);
    return Array.from({ length: pageCount }, (_, i) => i + 1);
  }

  protected readonly Math = Math;

  // Clean up on component destroy
  ngOnDestroy(): void {
    this.removeModalClass();
    this.searchSubject.complete();
  }
}
