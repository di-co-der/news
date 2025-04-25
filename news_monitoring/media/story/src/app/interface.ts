export interface Story {
  id: number;
  title: string;
  content: string;
  published_date: string;
  url: string;
  tagged_companies: Company[] | null;
}

export interface Company {
  id: number;
  name: string;
}
