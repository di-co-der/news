import {NgModule} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {MatButtonModule} from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';

import {NgSelectModule} from '@ng-select/ng-select';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {CookieService} from 'ngx-cookie-service';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import {ToastrModule} from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AddOrUpdateComponent } from './add-or-update/add-or-update.component';
import { DeleteComponent } from './delete/delete.component';
import { FetchStoriesComponent } from './fetch-stories/fetch-stories.component';


@NgModule({
  declarations: [
    AppComponent,
    AddOrUpdateComponent,
    DeleteComponent,
    FetchStoriesComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    TooltipModule.forRoot(),
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    NgSelectModule,
    BrowserAnimationsModule,
    NgbModule,
    ToastrModule.forRoot({
          timeOut: 3000,
          positionClass: 'toast-top-right',
          preventDuplicates: true,
          toastClass: 'ngx-toastr',
          titleClass: 'toast-title',
          messageClass: 'toast-message',
          tapToDismiss: true,
          progressBar: true,
          closeButton: true
            }),
    MatAutocompleteModule,
    MatChipsModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatButtonModule,
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
