import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import Swal from 'sweetalert2';


/*
*  @description :: Common service to send any AJAX requests.
*/

/*const apiURL = 'http://192.168.99.100:1330';*/
const apiURL = 'http://127.0.0.1:1331';

var httpOptions = {
  headers: new HttpHeaders({ 'enctype': 'multipart/form-data' })
};

@Injectable({
  providedIn: 'root'
})

export class StoreService {
  url: string;

  constructor(private http: HttpClient) {

  }

  private handleError(error: HttpErrorResponse) {
    // Error entry point for all AJAX request made using store

    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {

      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error.message}`);
      Swal.fire('Oops..', error.error.message, 'error')

    }
    return throwError('Something went wrong; please try again later.');
  };

  post(endpoint, data = {}, otherOptions = {}) {
    this.url = `${apiURL}${endpoint}`;
    httpOptions = Object.assign(httpOptions, otherOptions);
    return this.http.post(this.url, data, httpOptions)
      .pipe(
        tap(data => console.log('Request successful')),
        catchError(this.handleError)
      );
  }

  get(endpoint, data = {}, otherOptions = {}) {
    this.url = `${apiURL}${endpoint}`;
    httpOptions = Object.assign(httpOptions, otherOptions);
    return this.http.get(this.url, httpOptions)
      .pipe(
        tap(_ => console.log('Request successful')),
        catchError(this.handleError)
      );
  }
}
