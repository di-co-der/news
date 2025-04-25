import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import { Source } from '../interface';
import { SourceService } from '../http_service/source.service';


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

  constructor(
    public activeModal: NgbActiveModal,
    private fb: FormBuilder,
    private sourceService: SourceService,
    private toastr: ToastrService
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
        // Add more fields as needed
      });
    }
  }

  save(): void {
    if (this.sourceForm.invalid) return;

    const sourceData: Source = this.sourceForm.value;

    if (this.editMode && this.source) {
      this.sourceService.edit(this.source.id, sourceData).subscribe({
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
    } else {
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
}
