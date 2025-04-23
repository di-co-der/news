import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {CookieService} from 'ngx-cookie-service';

export interface Source {
  id: number;
  name: string;
  url: string;
  tagged_companies: string[] | null | undefined;
}

export interface SourceResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Source[];
}


@Injectable({
  providedIn: 'root'
})

export class SourceService {
  private baseUrl = 'http://127.0.0.1:8000/api-source/sources/';

  constructor(private http: HttpClient, private cookieService: CookieService) {}

// In your SourceService class
getSources(page: number = 1, searchQuery: string = ''): Observable<SourceResponse> {
  let params = new HttpParams();

  params = params.set('page', page.toString());

  if (searchQuery && searchQuery.trim() !== '') {
    params = params.set('search', searchQuery.trim());
  }

  console.log('Requesting sources with params:', params.toString());
  return this.http.get<SourceResponse>(`${this.baseUrl}`, { params });
}

  // fetchStory(sourceId: number): Observable<any> {
  //   const url = `${this.baseUrl}${sourceId}/fetch-stories/`;
  //   return this.http.get<{detail: string}>(url);
  // }

  fetchStory(sourceId: number): Observable<any> {
  const url = `${this.baseUrl}${sourceId}/fetch-stories/`;
  return this.http.get<{detail: string, stories: any[]}>(url);
}

  getSourceFormData(sourceId?: number | null) {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    const url = sourceId
      ? `${this.baseUrl}form-data/?source_id=${sourceId}`
      : `${this.baseUrl}form-data/`;
    return this.http.get(url, {headers, withCredentials: true });
  }

  createSource(data: any) {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
       // Make sure company is included in the source data
    if (!data.company) {
      // Get the user's company from local storage or another service
      // For now, we'll assume the user's company is available from a user service
      // or you can fetch it first before creating the source
      const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
      data.company = user.company?.id;
    }

    return this.http.post(this.baseUrl, data, { headers, withCredentials: true });
  }

  updateSource(id: number, data: any) {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
        if (!data.company) {
      // Get the user's company from local storage or another service
      // For now, we'll assume the user's company is available from a user service
      // or you can fetch it first before creating the source
      const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
      data.company = user.company?.id;
    }
    return this.http.put(`${this.baseUrl}${id}/`, data, {headers, withCredentials: true });
  }

    deleteSource(sourceId: number): Observable<any> {
    const url = `${this.baseUrl}${sourceId}/`;
     // Fetch CSRF token from cookie
    const csrfToken = this.cookieService.get('csrftoken');

    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });

    return this.http.delete(url, { headers, withCredentials: true });
  }

  // In your source.service.ts
  getCompanies() {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    // Use a different endpoint that only returns companies
    const url = 'http://127.0.0.1:8000/api-company/companies/';
    return this.http.get<any[]>(url, {headers, withCredentials: true });
  }
}
