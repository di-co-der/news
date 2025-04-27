export interface Story {
  id: number;
  title: string;
  body_text: string;
  published_date: string;
  article_url: string;
  tagged_companies: Company[] | null;
}

export interface Company {
  id: number;
  name: string;
}
