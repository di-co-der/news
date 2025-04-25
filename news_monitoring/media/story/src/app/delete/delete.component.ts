import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Story} from '../interface';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {StoryService} from '../http-service/story.service';
import {ToastrService} from 'ngx-toastr';

@Component({
  selector: 'app-delete',
  standalone: false,
  templateUrl: './delete.component.html',
  styleUrl: './delete.component.css'
})
export class DeleteComponent {
  @Input() story?: Story;
  @Output() refreshStories = new EventEmitter<void>();

  constructor(
    public activeModal: NgbActiveModal,
    private storyService: StoryService,
    private toastr: ToastrService
  ) {}

  delete(){
    if (!this.story) return;
    this.storyService.delete(this.story.id).subscribe({
      next: () => {
        console.log("inside delete")
        this.toastr.success('Source deleted successfully', 'Success');
        this.refreshStories.emit();
        this.activeModal.close('Delete');
      },
      error: (error) => {
        console.error('Error deleting source:', error);
        this.toastr.error('Failed to delete source', 'Error');
      }
    });
  }
}
