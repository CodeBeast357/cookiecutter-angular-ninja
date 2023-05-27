export interface IManagedAccountDictionary {
    [key: string]: IManagedAccount;
}

export interface IManagedAccount {
    id: number,
    source_company_key: string,
    source_company_database: string,
    name: string,
    username: string,
    role: string,
    warehouse: string,
    account_url: string,
    comment: string,
    status_code: number,
    warehouse_created: boolean,
    current_share: string
}

export interface IManagedAccountResponse {
    items: IManagedAccount[],
    count: number
}

export interface INewManagedAccountInput {
    name: string,
    database: string
}

export interface INewManagedAccountStatus {
    color: string,
    message: string
}