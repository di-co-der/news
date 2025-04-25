import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import {Company, Source} from '../interface';
import { SourceService } from '../http_service/source.service';
import {CommonService} from '../http_service/common.service';
import {map, Observable, of, switchMap} from 'rxjs';
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

  selectedCompany?: Company;
  companies: Company[] = [];

  constructor(
    public activeModal: NgbActiveModal,
    private fb: FormBuilder,
    private sourceService: SourceService,
    private toastr: ToastrService,
    private commonService: CommonService
  ) {
    this.sourceForm = this.fb.group({
      name: ['', Validators.required],
      url: ['', [Validators.required, Validators.pattern('https?://.*')]]
    });
  }

  ngOnInit(): void {
    if (this.source) {
      this.editMode = true;
      this.sourceForm.patchValue({
        name: this.source.name,
        url: this.source.url
      });
    }
    this.commonService.getCompanies().subscribe({
    next: (companies) => {
      this.companies = companies;
    },
    error: (err) => {
      console.error('Failed to load companies:', err);
    }
  });
  }

  save(): void {
  if (this.sourceForm.invalid) return;
  const sourceData: Source = this.sourceForm.value;
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
