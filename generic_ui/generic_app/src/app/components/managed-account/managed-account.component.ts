import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { IManagedAccount } from 'src/app/interfaces/managedaccount';
import { Observable, Subscription, switchMap, timer } from 'rxjs';



const baseAPIURL = 'http://ad-hoc.localhost/api/'
const managedAccountApiUrl = baseAPIURL + 'reader_accounts/'
const managedWarehouseApiUrl = baseAPIURL + 'create-ad-hoc-account-warehouse/'
const createOrUpdateManagedDatabaseApiUrl = baseAPIURL + 'update-account-database/'
const updateAccountAvailabilityUrl = baseAPIURL + 'update-account-availability/'

class ManagedAccount {
  id: number = 0;
  source_company_key: string = '';
  source_company_database: string = '';
  name: string = '';
  username: string = '';
  role: string = '';
  warehouse: string = '';
  account_url: string = '';
  comment: string = '';
  status_code: number = 403;
  warehouse_created: boolean = false;
  current_share: string = '';
}

@Component({
  selector: 'app-managed-account',
  templateUrl: './managed-account.component.html',
  styleUrls: ['./managed-account.component.scss']
})
export class ManagedAccountComponent implements OnInit {
  @Input() account: ManagedAccount = {
    id: -1,
    source_company_key: 'Loading...',
    source_company_database: 'Loading...',
    name: 'Loading...',
    username: 'Loading...',
    role: 'Loading...',
    warehouse: 'Loading...',
    account_url: 'Loading...',
    comment: 'Loading...',
    status_code: -1,
    warehouse_created: false,
    current_share: 'Loading...'
  };
  @Output() close = new EventEmitter();
  error: any;
  navigated = false; // true if navigated here
  subscription: Subscription = new Subscription;

  constructor (
    private route: ActivatedRoute,
    private http: HttpClient, 
  ) {}

  

  ngOnInit(): void {
    this.route.params.forEach((params: Params) => {
      if (params['id'] !== undefined) {
        const id = +params['id'];
        this.navigated = true;
        this.getAccountDetails(id);
      } else {
        this.navigated = false;
        this.account = new ManagedAccount();
      }
    });
  }


  getAccountDetails(id: number) {
    console.log("Getting managed accounts from the API.")
    this.subscription = this.http.get<IManagedAccount>(managedAccountApiUrl + id.toString())
        .subscribe(
          (account: IManagedAccount) => {
            this.account = account;
            console.log(account);
            }
        )
  }

  createWarehouse(id: number) {
    console.log("Creating warehouse for ID : ", id);
    this.subscription = this.http.post<IManagedAccount>(managedWarehouseApiUrl, {id: id})
        .subscribe(
          (account: IManagedAccount) => {
            console.log("Response: ", account)
            account.id = id;
            this.account = account;
            return account;
          }
        )
  }

  createOrUpdateShare(id: number) {
    console.log("Creating or updating database for for ID : ", id);
    this.subscription = this.http.post<IManagedAccount>(createOrUpdateManagedDatabaseApiUrl, {id: id})
        .subscribe(
          (account: IManagedAccount) => {
            console.log("Response: ", account)
            account.id = id;
            this.account = account;
            return account;
          }
        )
  }

  updateAccountAvailability(id: number) {
    console.log("Updating availability for ID : ", id);
    this.subscription = this.http.post<IManagedAccount>(updateAccountAvailabilityUrl, {id: id})
        .subscribe(
          (account: IManagedAccount) => {
            console.log("Response: ", account)
            account.id = id;
            this.account = account;
            return account;
          }
        )
  }

  // save(): void {
  //   this.heroService.save(this.hero).subscribe(hero => {
  //     this.hero = hero; // saved hero, w/ id if new
  //     this.goBack(hero);
  //   }, error => (this.error = error)); // TODO: Display error message
  // }

  // goBack(savedHero: Hero = null): void {
  //   this.close.emit(savedHero);
  //   if (this.navigated) {
  //     window.history.back();
  //   }
  // }




}
