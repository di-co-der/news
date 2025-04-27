import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import { Company, Story } from '../interface';
import { StoryService } from '../http-service/story.service';
import { CommonService } from '../http-service/common.service';

@Component({
  selector: 'app-add-or-update',
  standalone: false,
  templateUrl: './add-or-update.component.html',
  styleUrl: './add-or-update.component.css'
})
export class AddOrUpdateComponent implements OnInit {
  @Input() story?: Story;
  @Output() refreshStories = new EventEmitter<void>();

  storyForm: FormGroup;
  editMode = false;

  companies: Company[] = [];
  filteredCompanies: Company[] = [];
  selectedCompanies: Company[] = [];
  searchTerm = new FormControl('');

  constructor(
    public activeModal: NgbActiveModal,
    private fb: FormBuilder,
    private storyService: StoryService,
    private toastr: ToastrService,
    private commonService: CommonService
  ) {
    this.storyForm = this.fb.group({
      title: ['', Validators.required],
      body_text: ['', Validators.required],
      published_date: ['', Validators.required],
      article_url: ['', [Validators.required, Validators.pattern('https?://.*')]]
    });
  }

  ngOnInit() {
    // Load existing data if in edit mode
    if (this.story) {
      this.editMode = true;
      this.storyForm.patchValue({
        title: this.story.title,
        body_text: this.story.body_text,
        published_date: this.story.published_date,
        article_url: this.story.article_url
      });
      // If the story has tagged companies, load them
      if (this.story.tagged_companies) {
        this.selectedCompanies = this.story.tagged_companies;
      }
    }
    // Load all companies
    this.loadCompanies();
  }

  // Load all available companies
  loadCompanies() {
    this.commonService.getCompanies().subscribe({
      next: (response) => {
        this.companies = response.results || [];
        this.filteredCompanies = [...this.companies];
        // Filter out already selected companies
        if (this.selectedCompanies.length > 0) {
          this.filteredCompanies = this.companies.filter(company =>
            !this.selectedCompanies.some(c => c.id === company.id)
          );
        }
      },
      error: (err) => {
        console.error('Failed to load companies:', err);
        this.toastr.error('Failed to load companies', 'Error');
      }
    });
  }

  search(term: string | null) {
    const searchText = term || '';
    // If no search term, show all unselected companies
    if (!searchText.trim()) {
      this.filteredCompanies = this.companies.filter(company =>
        !this.selectedCompanies.some(c => c.id === company.id)
      );
      return;
    }
    // Filter companies that match the search term and aren't already selected
    this.filteredCompanies = this.companies.filter(company =>
      company.name.toLowerCase().includes(searchText.toLowerCase()) &&
      !this.selectedCompanies.some(c => c.id === company.id)
    );
  }

  // Select a company if not already selected
  selectCompany(company: Company) {
    // Check if company is already selected
    const isAlreadySelected = this.selectedCompanies.some(c => c.id === company.id);
    if (!isAlreadySelected) {
      // Add to selected companies
      this.selectedCompanies.push(company);
      this.searchTerm.setValue('');  // Clear search input
      // Update filtered companies to remove selected ones
      this.filteredCompanies = this.companies.filter(c =>
        !this.selectedCompanies.some(selected => selected.id === c.id)
      );
    }
  }

  // Remove a company from selected companies
  removeCompany(company: Company) {
    this.selectedCompanies = this.selectedCompanies.filter(c => c.id !== company.id);
    this.search(this.searchTerm.value || '');
  }

  save() {
    if (this.storyForm.invalid) return;
    const storyData = {...this.storyForm.value};
    const storyPayload = {
      title: storyData.title,
      body_text: storyData.body_text,
      published_date: storyData.published_date,
      article_url: storyData.article_url,
      tagged_companies: this.selectedCompanies.map(company => company.id)
    };

    if (this.editMode && this.story) {
      this.update(this.story.id, storyPayload);
    } else {
      this.add(storyPayload);
    }
  }

  private update(id: number, storyPayload: any): void {
    this.storyService.edit(id, storyPayload).subscribe({
      next: () => {
        this.toastr.success('Story updated successfully', 'Success');
        this.refreshStories.emit();
        this.activeModal.close('Save');
      },
      error: (error) => {
        console.error('Error updating story:', error);
        this.toastr.error('Failed to update story', 'Error');
      }
    });
  }

  private add(storyPayload: any): void {
    this.storyService.add(storyPayload).subscribe({
      next: () => {
        this.toastr.success('Story added successfully', 'Success');
        this.refreshStories.emit();
        this.activeModal.close('Save');
      },
      error: (error) => {
        console.error('Error adding story:', error);
        this.toastr.error('Failed to add story', 'Error');
      }
    });
  }
}
