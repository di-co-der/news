import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

export const csrfInterceptor: HttpInterceptorFn = (req, next) => {
  // Only add the CSRF token for state-changing methods (POST, PUT, DELETE, etc.)
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    const cookieService = inject(CookieService);
    const csrfToken = cookieService.get('csrftoken');

    if (csrfToken) {
      req = req.clone({
        setHeaders: {
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      });
    }
  }
  return next(req);
};
