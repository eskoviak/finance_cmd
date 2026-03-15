# Data Modeling Notes: MyFinance Application

**Revision History**
| | |
|--|--|
| 2026-03-10 | Original -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-03-14 | Added Register map Excel --> finance.register -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |

**Data Entities**
| | |
|---|---|
| **PostgreSQL Database** | `finance` |

---

** Register Conversion

Create a mapping routine to read the data From Excel (`/Users/edmundlskoviak/iCloud/Documents/Excel/Banking.xlsx`) to insert into the finance.register table.  There are currently two tables to be converted:

1. CapOneRegister
2. Sch_010z_Register

| Excel Column Name | Transformatiom | finance.application | Notes |
|--|--|--|--|
| -- | -- |id : sequence not null| no mapping, handled by engine during insert |
| Account | ??? |external_account_id : integer||
| Code | -- |code : integer||
| Date | Excel Date to ... |date : timestamp with time zone not null| |
| Description | -- |description : varchar(100)||
| Debit(-) | -- |debit : numeric(10,2)||
| IsFee | -- | isFee : boolean||
| Credit(-) | -- |credit : numeric(10,2)||
| Transnum | -- |tran_no : integer||
| Reconciled | -- |reconciled : boolean||
| Voucher | -- |voucher : integer||

*** Notes on finance.register.voucher

This field represents the id of the transaction details, which points to different table depending on the value of code.

| code | name | id points to table |
|--|--|--|
| 1 | Check | voucher  |   
| 2 | Debit Card | voucher  |
| 3 | Teller w/d | voucher  |
| 4 |ACH Payment | voucher  |
| 5 | Transfer | asset_transfer  |
| 6 | Interest | ???  |
| 7 | Direct Deposit | asset_transfer  |
| 8 | ATM Withdrawl | voucher  |
| 10 | ATM Fee | voucher, isFee = T  |
| 11 | Adjustment | ???
| 12 | Brokerage | voucher, transnum = Symbol  |
| 13 | Equities Dividend | asset_transfer ???  |
| 14 | Electronic Deposit | asset_transfer  |
| 15 | Maintenance Fees | voucher  |
| 16 | IRA Payout | asset_transfer  |
| 17 | Advisor Fee | ??? is this 15 |

