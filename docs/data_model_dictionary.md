# Data Model and Dictionary: MyFinance Application

## Revision History

| Date | Change |
| -- | -- |
| 2026-03-10 | Original -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-03-14 | Added Register map Excel --> finance.register -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-03-31 | Updated and condensed in model notes -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-04-23 | Updated data model to add account_transfers table -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) and other general edits |

## References

[Master Account Layout](https://docs.google.com/spreadsheets/d/11EeBdlk-c77F0ZfZZRRzI46cIuj8fUo-xT5nSF0o8Nk/edit?usp=sharing)

## Data Entities

| Data Store | Collection  |
| --- | --- |
| [PostgreSQL](out/MyFinance-data-class/myfinance-data-class.png) | `finance` |
---

## Register Conversion

**NOTE** Currently, in the Schwab and CapOne registers, the columns labeled Debit(-) and Credit(+) are reversed.  This should be fixed in the database convers

Create a mapping routine to read the data From Excel (`/Users/edmundlskoviak/iCloud/Documents/Excel/Banking.xlsx`) to insert into the finance.register table.  There are currently two tables to be converted:

1. CapOneRegister
2. Sch_010z_Register

The following will not be transfered:

1. AMEX HYSA or Rewards Checking.  These have been (Rewards Checking) or will be closed (HYSA).
2. Amerirpise will be closed by end of march.

| Excel Column Name | Transformatiom | finance.application | Notes |
|--|--|--|--|
| -- | -- |id : sequence not null| no mapping, handled by engine during insert |
| Account | -- |external_account_id : integer||
| Code | -- |code : integer||
| Date | Excel Date to target column type |date : timestamp with time zone not null| |
| Description | -- |description : varchar(100)||
| Debit(-) | -- | credit : numeric(10,2)||
| IsFee | -- | isFee : boolean||
| Credit(-) | -- | debit : numeric(10,2)||
| Transnum | Converted to text and moved to memo |--||
| Reconciled | -- |reconciled : boolean||
| Voucher | -- |voucher : integer||
| -- | -- | memo : text ||
| -- | -- | category_id : integer ||

*** Notes on finance.register.voucher

This field represents the id of the transaction details, which points to different table depending on the value of code.

| code | name | id points to table | Description |
|--|--|--|--|
| 1 | Check | voucher.voucher_number  | A physical check.  The number should be recorded in the memo field.  |
| 2 | Debit Card | voucher.voucher_number  ||
| 3 | Teller w/d | voucher.voucher_number  | Base amount in credit column, separate entry for fee |
| 4 | ACH Payment | voucher.voucher_number  ||
| 5 | Transfer | asset_transfer.id ||
| 6 | Interest | ???  ||
| 7 | Direct Deposit | asset_transfer  ||
| 8 | ATM Withdrawl | voucher  | Base amount in credit column, separate entry for fee |
| 10 | ATM Fee | voucher, isFee = T  ||
| 11 | Adjustment | ???  ||
| 12 | Brokerage | asset_transfer (src of funds, holding account), memo = Symbol  ||
| 13 | Equities Dividend | revenue ???  ||
| 14 | Electronic Deposit | asset_transfer  ||
| 15 | Maintenance Fees | voucher  ||
| 16 | IRA Payout | asset_transfer  ||
| 17 | Advisor Fee | Fee paid to Advisor ||

The following will be used to update external_accounts.account_type

| Code | Meaning and Usage |
| -- | --- |
| CH | Checking |
| DB | Debit account |
| BRK | Brokerage  Account |
| SAV | Savings Account |
| CC | Credit Card |
| LN | Loan |
| HSA  | Health Savings Account |
| IRA | Individual Retirement Account |
| INV | Investment Account (institutional ) |

Cleanup is necessary on this table as well, notably real account numbers (perhaps table need to be encrypted?)  Probably need to add Active column (This was completed with Issue 30).

## Data Cleanup `external_accounts` (Issue 42)

There are a number of records (196) assigend to external_account_id 19970 (Capital One Debit). These also have a a payment_type_id of 10 (debit).  These should be 10207 (which is what appears on receipts).  There are also a few assigned to external_acocunt_id 17542, which is the base checking account.  They need to also be moved to 10207.  To correct:
1. Add a new external_account_id for Capital One Debit (10207) at 
2. Move all records with (external_account_id = 19970 AND payment_type_id = 10) to 10207
3. Check that all records moved from 19970
4. Repeat for external_account_id = 17542 and payment_type_id = 10.
5. Check that all records moved from 17542
6. Removed entry 19970 from external_accounts table.

There are records of which match both cases in finance_tst.  Develop the scripts there and test.

## Revenue Accounts

When we created the application, the revenue accounts were stored with the external_accounts table.  These should be moved to a revenue table.  Do the following:

1.  Income from LMC and SSA:  This is account type 040202 (revenue recognized over time -- services).  There is currently an entry in `external_accounts` called 'Pension Income' (42202).  Use this account as the source in `asset_transfers`; indicate in the memo column the exact source--be specific, e.g. 'LMC Pension', 'SSA Survivor Benefit'.
2. Using this strategy, a separte revenue table may not be necessary.
3. Income from Brokerage dividends:  Use account 14100 (cap gains and dividends) as the source in `asset_transfers`; indicate in the memo column the exact source--ticker symbol.

# Modeling Common Events

## Debit Card Payments for Goods and Services

These are entries in the register (expense) and a corresponding credit in the asset register.  The transaction is composed of two lines in the combined dataset, but only one in the final application tables.

Traditionally, this would be modeled as:
1. A debit to expense (05XXXX)
2. A credit to the asset (01XXXX)

Currently, there is no general ledger in the application, we do record the credit in the register table at the time of the transaction.  This is not ideal, but it is the current implementation.  As the application evolves, this will need to be revisited.  See the note in the Schema Creation section regarding the reversal of debit/credit columns in the Schwab and CapOne registers.  Note exact expense account **IS** carried in the voucher detail (voucher_detail.account_number, .dimension_1 and .dimension_2). From this we can construct a true Ledger entry for each transaction.

## Transfers Between Accounts

This mostly occurs between Schwab and CapOne, though it may occcur with other accounts as well.  The key, as far as the model is concerned, is that this is a transfer between two accounts.  The transaction should be recorded as a credit in one account and a debit in the other.  It should not be recorded as an expense or income. There are several *possible* targets in CapOne:  Checking and Savings (CapOne pays itself one the two credit card accounts).

The `finance.asset_transfer` table is used.  The .id column is auto populated.
- .transfer_date:  the effective date of the transfer, *i.e.* '4/20/2026'
- .transfer_amt: The value of the transaction 
- .src_external_account_id: the 5 digit account from `external_accounts` to be credited.
- .tgt_external_account_id: the 5 digit account from `external_accounts` to be debited.
- .memo: a description of the transaction

There is currently no support for this functionality in the application.  Transfers are entered manually into the `finance.asset_transfer` table.  Issue #43 has bee created to add this functionality.

## Accounts Payable

This table is currely used to track ACH transactions which have been set-up to autopay from Cash (CapOne) or added as an expense on a credit card account (CapOne 22301).  Ultimately, it should reflect all future payments (open AP) which are known and expected.  This has been implemented in the branch '30-database-changes' and tested on tech-test, but yet deployed to production.


## Revenue Recognition

### SSA Payments

### LMC Pension

## Schwab Distributions


## Liabilities

