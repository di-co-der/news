import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {RouterOutlet} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';

import {ToastrModule} from 'ngx-toastr';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AddOrUpdateComponent } from './add-or-update/add-or-update.component';
import { DeleteComponent } from './delete/delete.component';


@NgModule({
  declarations: [
    AppComponent,
    AddOrUpdateComponent,
    DeleteComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterOutlet,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
