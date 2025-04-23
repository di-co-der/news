// src/app/services/story.service.ts

import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

export interface Story {
  id: number;
  title: string;
  article_url: string;
  body_text: string;
  published_date: string;
  tagged_companies: string[] | null | undefined;
  company: number;
  company_name: string;
  source_details?: {
    id: number;
    name: string;
    url: string;
  };
}

export interface StoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Story[];
}

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  private baseUrl = 'http://127.0.0.1:8000/api-story/stories/';

  constructor(private http: HttpClient, private cookieService: CookieService) {}

  getStories(page: number = 1, searchQuery: string = ''): Observable<StoryResponse> {
    let params = new HttpParams();

    params = params.set('page', page.toString());

    if (searchQuery && searchQuery.trim() !== '') {
      params = params.set('search', searchQuery.trim());
    }

    console.log('Requesting stories with params:', params.toString());
    return this.http.get<StoryResponse>(`${this.baseUrl}`, { params });
  }

  getStoryById(storyId: number): Observable<Story> {
    return this.http.get<Story>(`${this.baseUrl}${storyId}/`);
  }

  getStoryFormData(storyId?: number | null) {
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });
    const url = storyId
      ? `${this.baseUrl}form-data/?story_id=${storyId}`
      : `${this.baseUrl}form-data/`;
    return this.http.get(url, { headers, withCredentials: true });
  }

  // In StoryService - createStory method
createStory(data: any) {
  const csrfToken = this.cookieService.get('csrftoken');
  const headers = new HttpHeaders({
    'X-CSRFToken': csrfToken,
    'Content-Type': 'application/json'
  });

   if (!data.company) {
      // Get the user's company from local storage or another service
      // For now, we'll assume the user's company is available from a user service
      // or you can fetch it first before creating the source
      const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
      data.company = user.company?.id;
    }
    return this.http.post(this.baseUrl, data, { headers, withCredentials: true });
  }

// In StoryService - updateStory method
updateStory(id: number, data: any) {
  const csrfToken = this.cookieService.get('csrftoken');
  const headers = new HttpHeaders({
    'X-CSRFToken': csrfToken,
    'Content-Type': 'application/json'
  });

  const cleanData = { ...data };

  // Only handle tagged_companies conversion
  if (cleanData.tagged_companies && Array.isArray(cleanData.tagged_companies)) {
    cleanData.tagged_companies = cleanData.tagged_companies.map((id: string | number) =>
      typeof id === 'string' ? parseInt(id, 10) : id
    );
  }

  const safeData = JSON.parse(JSON.stringify(cleanData));

  console.log('Sending update data with PATCH:', safeData);
  // Use PATCH instead of PUT
  return this.http.patch(`${this.baseUrl}${id}/`, safeData, { headers, withCredentials: true });
}

  deleteStory(storyId: number): Observable<any> {
    const url = `${this.baseUrl}${storyId}/`;
    const csrfToken = this.cookieService.get('csrftoken');
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });

    return this.http.delete(url, { headers, withCredentials: true });
  }

  getStoriesBySource(sourceId: number, page: number = 1): Observable<StoryResponse> {
    let params = new HttpParams();
    params = params.set('page', page.toString());
    params = params.set('source', sourceId.toString());

    return this.http.get<StoryResponse>(`${this.baseUrl}`, { params });
  }
}
