import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import {Source} from '../interface';


@Injectable({
  providedIn: 'root'
})
export class SourceService {
  private baseUrl = 'http://127.0.0.1:8000/api-source/';

  constructor(private http: HttpClient) {}

  search(page: number = 1, query: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString());
    if (query && query.trim() !== '') {
      params = params.set('search', query.trim());
    }
    return this.http.get(`${this.baseUrl}`, { params });
  }

  add(source: Source): Observable<any> {
    return this.http.post(this.baseUrl, source);
  }

  edit(id: number, source: Source): Observable<any> {
    return this.http.put(`${this.baseUrl}${id}/`, source);
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}${id}/`);
  }

  fetchStories(sourceId: number): Observable<any> {
  const url = `${this.baseUrl}${sourceId}/fetch-stories/`;
  return this.http.get<{detail: string, stories: any[]}>(url);
  }
}
