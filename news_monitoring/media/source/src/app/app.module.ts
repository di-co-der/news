import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, NgModel, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';

import {CookieService} from 'ngx-cookie-service';
import { TooltipModule } from 'ngx-bootstrap/tooltip';

import {NgSelectModule} from '@ng-select/ng-select';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ViewSourcesComponent } from './view-sources/view-sources.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {NgModule} from '@angular/core';


@NgModule({
  declarations: [
    AppComponent,
    ViewSourcesComponent,
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
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
