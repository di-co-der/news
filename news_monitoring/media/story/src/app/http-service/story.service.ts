import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import {Story} from '../interface';

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  private baseUrl = 'http://127.0.0.1:8000/api-story/';

  constructor(private http: HttpClient) {}
  search(page: number = 1, query: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString()); //another method

    if (query && query.trim() !== '') {
      params = params.set('search', query.trim());
    }
    return this.http.get(`${this.baseUrl}`, { params });
  }

  add(story: Story): Observable<any> {
    return this.http.post(this.baseUrl, story);
  }

  edit(id: number, story: Story): Observable<any> {
    return this.http.put(`${this.baseUrl}${id}/`, story);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}${id}/`);
  }
}
