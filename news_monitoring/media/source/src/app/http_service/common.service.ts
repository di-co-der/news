import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

import {map, Observable} from 'rxjs';
import {CookieService} from 'ngx-cookie-service';

import {Company} from '../interface';


@Injectable({
  providedIn: 'root'
})
export class CommonService {

  private baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient, private cookieService: CookieService) {}

  getCompanies(): Observable<Company[]> { //search companies
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    return this.http.get<{ results: Company[] }>(`${this.baseUrl}api-company/companies/`, {
        headers,
        withCredentials: true
      }).pipe(
        map(response => response.results)
      );
  }
}
