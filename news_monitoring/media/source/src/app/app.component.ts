import {Component, OnInit} from '@angular/core';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';

import { Observable, Subject } from 'rxjs';
import { debounceTime, map, startWith } from 'rxjs/operators';
import { ToastrService } from 'ngx-toastr';

import {Source, SourceResponse} from './interface';
import {SourceService} from './http_service/source.service';
import {Router} from '@angular/router';


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

  searchQuery: string = '';

  constructor(
    private sourceService: SourceService,
    private router: Router,
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
        next: (response: SourceResponse) => {
          this.sources = response.results;
          this.totalItems = response.count;
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
    this.router.navigate(['/sources/add-or-update']);
  }

  edit(source: Source) {
    this.router.navigate(['/sources/add-or-update', source.id]);
  }

  delete(source: Source){
    if (confirm('Are you sure you want to delete this source?')) {
      this.sourceService.delete(source.id).subscribe({
        next: () => {
          this.toastr.success('Source deleted successfully', 'Success');
          this.fetchSources();
        },
        error: (error) => {
          console.error('Error deleting source:', error);
          this.toastr.error('Failed to delete source', 'Error');
        }
      });
    }
  }

  // Fetch stories from a source
  fetchStories(sourceId: number) {
    this.sourceService.fetchStories(sourceId).subscribe({
      next: (response) => {
        if (response && response.stories && response.stories.length > 0) {
          this.toastr.success(`${response.stories.length} stories fetched`, 'Success');
          // Show stories in modal or navigate to stories view
          this.router.navigate(['/sources/stories', sourceId]);
        } else {
          this.toastr.info('No new stories were found', 'Information');
        }
      },
      error: (error) => {
        console.error('Error fetching stories:', error);
        this.toastr.error('Failed to fetch stories', 'Error');
      }
    });
  }

// getCompanyNames(tagged_companies: Companies[] | undefined): string {
//   console.log("Function called");
//
//   if (!tagged_companies || tagged_companies.length === 0) {
//     return 'N/A';
//   }
//
//   const names = tagged_companies.map(company => company.name).join(', ');
//   console.log("Companies:", names);
//   return names;
// }


  protected readonly Math = Math;
}
