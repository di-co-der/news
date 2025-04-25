import { Injectable } from '@angular/core';
import {Companies} from '../interface';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {CookieService} from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class CommonService {

  private baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient, private cookieService: CookieService) {
  }

  getCompanies(): Observable<Companies[]> { //search companies
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });

    return this.http.get<Companies[]>(`${this.baseUrl}api-company/companies/`, {
      headers,
      withCredentials: true
    });
  }
}
