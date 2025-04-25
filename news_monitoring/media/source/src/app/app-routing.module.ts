import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AppComponent} from './app.component';
import {AddOrUpdateComponent} from './add-or-update/add-or-update.component';


const routes: Routes = [
  { path: 'sources/add', component: AddOrUpdateComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: false })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
