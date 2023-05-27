import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { Observable, Subscription, switchMap, timer } from 'rxjs';
import { IStatus } from 'src/app/interfaces/istatus';
import { IManagedAccount, IManagedAccountDictionary, IManagedAccountResponse, INewManagedAccountInput} from 'src/app/interfaces/managedaccount';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { take } from 'rxjs/operators';


const baseAPIURL = 'http://ad-hoc.localhost/api/'
const statusURL = baseAPIURL + 'status'
const managedAccountApiUrl = baseAPIURL + 'reader_accounts/?page='
const deleteManagedAccountApiUrl = baseAPIURL + 'reader_accounts'
const createManagedAccountApiUrl = baseAPIURL + 'create-ad-hoc-account/'
const getDatabasesUrl = baseAPIURL + 'get-available-databases/'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  
  snackbarDurationInSeconds = 5;
  status: IStatus = {'uptime': 0, 'mysql_connected': false};
  loadCount: number = 0;
  subscription: Subscription = new Subscription;
  managedAccounts: IManagedAccountDictionary = {}; 
  newManagedAccountForm!: FormGroup;
  isLoading = false;
  availableDatabases: string[] = [];
  selectedDatabase: string = '';

  constructor(
    private http: HttpClient, 
    private formBuilder: FormBuilder,
    private _snackBar: MatSnackBar
  )
  {
    this.getManagedAccounts()
  }

  ngOnInit() {
    this.getDatabases();
    this.newManagedAccountForm = this.formBuilder.group({
      name: ['', Validators.required],
      database: ['', Validators.required]
    });
  }

  openSnackBar(message: string) {
    this._snackBar.open(message, "Dismiss");
  }

  // This is pretty shitty.  The status bar isn't for getting managed account states, it's for having some accounts
  // loaded, which is ghetto as fuck when you have none, but that's a slim edge case, so I'mma let it slide for now.
  getManagedAccounts() {
    console.log("Getting managed accounts from the API.")
    this.subscription = this.http.get<IManagedAccountResponse>(managedAccountApiUrl + "1")
        .subscribe(
          (resp: IManagedAccountResponse) => {
            console.log(resp);
            resp.items.forEach(element => {
              this.managedAccounts[element.id] = element;
            });
            console.log('managedAccounts', this.managedAccounts);
            }
        )
  }

  updateManagedAccount(managedAccount: any) {
    // Implement the logic to handle form submission for each managed account
    console.log("Updating managed account values: ");
    console.log(managedAccount);
  }

  deleteManagedAccount(id: number) {
    console.log("Deleting managed account: ", id);
    this.isLoading = true;
    this.subscription = this.http.delete<string>(deleteManagedAccountApiUrl + "/" + id.toString())
        .subscribe(
          (resp: string) => {
            console.log('Deleted managed account', id, resp);
            delete this.managedAccounts[id];
            this.isLoading = false;
            this.openSnackBar(JSON.stringify(resp))
            return resp;
          }
        )
  }

  getDatabases() {
    console.log("Getting source databases");
    this.subscription = this.http.get<string[]>(getDatabasesUrl)
        .subscribe(
          (databases: string[]) => {
            console.log(databases);
            this.availableDatabases = databases;
            return databases;
          }
        )
  }

  createManagedAccount(newManagedAccount: INewManagedAccountInput) {
    console.log("Creating managed account: ", newManagedAccount);
    this.isLoading = true;
    const body=JSON.stringify(newManagedAccount);
    console.log(body);
    this.subscription = this.http.post<IManagedAccount>(createManagedAccountApiUrl, body)
        .subscribe(
          (resp: IManagedAccount) => {
            this.isLoading = false;
            console.log('Created managed account', newManagedAccount.name, resp);
            const message: string = "Created managed account: " + resp.account_url;
            this.managedAccounts[resp.name] = resp
            this.openSnackBar(JSON.stringify(message))
            return resp;
          }
        )
  }

  getStatusCodeColor(statusCode: number): string {
    return statusCode === 200 ? 'success' : 'warn';
  }

  getStatusCodeLabel(statusCode: number): string {
    return statusCode === 200 ? 'Ready' : 'Not Ready';
  }
}
