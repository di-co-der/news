import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ViewStoryComponent} from './view-story/view-story.component';


const routes: Routes = [
   { path: 'stories', component: ViewStoryComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
