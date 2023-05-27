import { Component, OnInit } from '@angular/core';
import { Observable, Subscription, switchMap, timer } from 'rxjs';
import { HttpClient } from '@angular/common/http';



const baseAPIURL = 'http://ad-hoc.localhost/api/'
const stringConfigURL = baseAPIURL + 'string_configs/?page=1'
const intConfigURL = baseAPIURL + 'int_configs/?page=1'

export interface IStringConfigs {
  items: IStringConfig[],
  count: number
}
export interface IStringConfig {
  id: number,
  title: string,
  value: string,
}

export interface IIntConfigs {
  items: IIntConfig[],
  count: number
}
export interface IIntConfig {
  id: number,
  title: string,
  value: BigInteger,
}


// TODO: https://stackblitz.com/edit/angular-custom-pagination-mat-table?file=src%2Fapp%2Ftable-basic-example.ts
// Implement an editable table for these.
@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {

  
  stringConfigList!: IStringConfigs;
  intConfigList!: IIntConfigs;
  subscription: Subscription = new Subscription;
  displayedColumns: string[] = ['id', 'title', 'value'];

  constructor(private http: HttpClient) { 
    
    this.getIntConfigs();
    this.getStringConfigs();
  }

  ngOnInit(): void {
  }

  getStringConfigs() {
    this.subscription = this.http.get<IStringConfigs>(stringConfigURL)
        .subscribe(
          resp => {
            this.stringConfigList = resp; 
            console.log('string_configs', resp);
            return resp;
          }
        )
  }

  getIntConfigs() {
    this.subscription = this.http.get<IIntConfigs>(intConfigURL)
        .subscribe(
          resp => {
            this.intConfigList = resp; 
            console.log('int_configs', resp);
            return resp;
          }
        )
  }

}
