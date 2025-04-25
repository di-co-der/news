import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';

import { Source } from '../interface';
import { SourceService } from '../http_service/source.service';


@Component({
  selector: 'app-delete',
  standalone: false,
  templateUrl: './delete.component.html',
  styleUrl: './delete.component.css'
})
export class DeleteComponent{
   @Input() source?: Source;
   @Output() refreshSources = new EventEmitter<void>();

  constructor(
    public activeModal: NgbActiveModal,
    private sourceService: SourceService,
    private toastr: ToastrService
  ) {}

  delete(){
    if (!this.source) return;
    this.sourceService.delete(this.source.id).subscribe({
      next: () => {
        this.toastr.success('Source deleted successfully', 'Success');
        this.refreshSources.emit();
        this.activeModal.close('Delete');
      },
      error: (error) => {
        console.error('Error deleting source:', error);
        this.toastr.error('Failed to delete source', 'Error');
      }
    });
  }
}
