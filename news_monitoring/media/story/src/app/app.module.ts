import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ViewStoryComponent } from './view-story/view-story.component';
import {RouterOutlet} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {ToastrModule} from 'ngx-toastr';

@NgModule({
  declarations: [
    AppComponent,
    ViewStoryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterOutlet,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
