import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import {Company, Source} from '../interface';
import { SourceService } from '../http_service/source.service';
import {CommonService} from '../http_service/common.service';
import {map, Observable, of, Subject, switchMap} from 'rxjs';
import {debounceTime} from 'rxjs/operators';


@Component({
  selector: 'app-add-or-update',
  standalone: false,
  templateUrl: './add-or-update.component.html',
  styleUrl: './add-or-update.component.css'
})
export class AddOrUpdateComponent implements OnInit{
  @Input() source?: Source;
  @Output() refreshSources = new EventEmitter<void>();

  sourceForm: FormGroup;
  editMode = false;

  companies: Company[] = [];
  filteredCompanies: Company[] = [];
  selectedCompanies: Company[] = [];
  searchTerm = new FormControl('');

  constructor(
    public activeModal: NgbActiveModal,
    private fb: FormBuilder,
    private sourceService: SourceService,
    private toastr: ToastrService,
    private commonService: CommonService
  ) {
    this.sourceForm = this.fb.group({
      name: ['', Validators.required],
      url: ['', [Validators.required, Validators.pattern('https?://.*')]],
      taggedCompanies: [[]]
    });
  }

  ngOnInit(){
    // Load existing data if in edit mode
    if (this.source) {
      this.editMode = true;
      this.sourceForm.patchValue({
        name: this.source.name,
        url: this.source.url
      });
      // If the source has tagged companies, load them
      if (this.source.tagged_companies) {
        this.selectedCompanies = this.source.tagged_companies as Company[];
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
  selectCompany(company: Company){
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
  if (this.sourceForm.invalid) return;
  const sourceData: Source = {...this.sourceForm.value};
  sourceData.tagged_companies = this.selectedCompanies;
  console.log(sourceData.tagged_companies)
  console.log(sourceData.name)
  if (this.editMode && this.source) {
    this.update(this.source.id, sourceData);
  } else {
    this.add(sourceData);
  }
}

  private update(id: number, sourceData: Source): void {
    this.sourceService.edit(id, sourceData).subscribe({
      next: () => {
        this.toastr.success('Source updated successfully', 'Success');
        this.refreshSources.emit();
        this.activeModal.close('Save');
      },
      error: (error) => {
        console.error('Error updating source:', error);
        this.toastr.error('Failed to update source', 'Error');
      }
    });
  }

  private add(sourceData: Source): void {
    this.sourceService.add(sourceData).subscribe({
      next: () => {
        this.toastr.success('Source added successfully', 'Success');
        this.refreshSources.emit();
        this.activeModal.close('Save');
      },
      error: (error) => {
        console.error('Error adding source:', error);
        this.toastr.error('Failed to add source', 'Error');
      }
    });
  }
}
