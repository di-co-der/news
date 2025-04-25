export interface User {
  id: number;
  name: string;
}

export interface Company { //company
  id: number;
  name: string;
}

export interface Source {
  id: number;
  name: string;
  url: string;
  added_by: User;
  updated_by: User;
  tagged_companies: Company[] | null;
}

export interface SourceResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Source[];
}
