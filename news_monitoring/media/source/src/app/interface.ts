interface Source {
  id: number;
  name: string;
  url: string;
  added_by: User;
  updated_by: User;
  tagged_companies: Companies[];
}

interface User {
  id: number;
  name: string;
}

interface Companies {
  id: number;
  name: string;
}
