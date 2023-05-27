import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { IStatus } from '../interfaces/istatus';
import { Observable } from 'rxjs';

const baseAPIURL = 'http://ad-hoc.localhost/api/'
const statusURL = baseAPIURL + 'status'


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
    ) { }

  getStatus(): Observable<IStatus> {
    // return of ({status: 'up', uptime: '1234', server_time: "Jan 1 1984"});
    const resp$ = this.http.get<IStatus>(statusURL);
    resp$.subscribe(status => console.log(status));
    return resp$;
  }

}