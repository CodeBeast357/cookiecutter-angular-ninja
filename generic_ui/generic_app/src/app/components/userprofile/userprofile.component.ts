import { Component, OnInit } from '@angular/core';
import { IProfile } from 'src/app/interfaces/iprofile';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription, switchMap, timer } from 'rxjs';


const baseAPIURL = 'http://ad-hoc.localhost/api/'
const statusURL = baseAPIURL + 'user_profile/1'



@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.scss']
})
export class UserprofileComponent implements OnInit {
  
  subscription: Subscription = new Subscription;
  profile: IProfile = {
    first_name: "default",
    last_name: "default",
    email: "default",
    about_me: "default"
  };

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getProfile()
  }

  getProfile() {
    this.subscription = this.http.get<IProfile>(statusURL)
        .subscribe(
          resp => {
            this.profile = resp; 
            console.log('resp', resp);
            return resp;
          }
        )
  }

}
