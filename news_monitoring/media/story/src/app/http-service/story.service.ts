import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

import {Story} from '../interface';

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  private baseUrl = 'http://127.0.0.1:8000/api-story/';

  constructor(private http: HttpClient, private cookieService: CookieService) {}
  search(page: number = 1, query: string = ''): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString()); //another method

    if (query && query.trim() !== '') {
      params = params.set('search', query.trim());
    }
    return this.http.get(`${this.baseUrl}`, { params });
  }

  add(story: Story): Observable<any> {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    return this.http.post(this.baseUrl, story, {
      headers,
      withCredentials: true
    });
  }

  edit(id: number, story: Story): Observable<any> {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    return this.http.put(`${this.baseUrl}${id}/`, story, {
      headers,
      withCredentials: true
    });
  }

  delete(id: number): Observable<any> {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    return this.http.delete(`${this.baseUrl}${id}/`, {
      headers,
      withCredentials: true
    });
  }
}
