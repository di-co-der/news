import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AppComponent} from './app.component';
// import {AddSourceComponent} from './add-source/add-source.component';
import {ViewSourcesComponent} from './view-sources/view-sources.component';


const routes: Routes = [
  { path: '', redirectTo: '/sources', pathMatch: 'full' },
  { path: 'sources', component: ViewSourcesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: false })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
