# Suggested Changes to external_accounts

Create scripts in `finance/scripts` to alter/update the table in both schemas (`finance` and `finance_tst`).

column `account_type` Needs to be updated for all records

column `active` Needs to be added to the tables and updated for all records

The Apple cards need to be updated to have the correct account_type and numbers.  Need to surveil existing vouchers to determine the current usage.

### *TODO* how to correct account_numbers without compromising data security (full account numbers is no go)

### *TODO* Once the `active` field is updated, the routine that build the account selector needs to be updated to only show active accounts.    


| external_account_id |             account_name              |      account_number       | qualified | account_type | active |
| --- | --- | --- | --- | --- | --- |
|               19383 | Altra Regular Share                   | 010101                    | N         | SA | Y |
|               10401 | Ameriprise Debit                      | 010101                    | N         |    | N |
|               17133 | Ameriprise One Financial Account      | 0000 4161 5785 7 133      | N         |    | N |
|               16133 | Ameriprise SPS ADV                    | 0000 6348 5852 6 133      | N         |    | N |
|               15133 | Ameriprise SPS ADV                    | 0000 8215 3184 5 133      | Q         |    | N |
|               12133 | Ameriprise SPS ADV                    | 0000 7491 8790 2 133      | Q         |    | N |
|               26624 | Ameriprise Visa                       | 020101                    |           |    | N |
|               18464 | Amerprise check                       | 010101                    | N         |    | N |
|               22008 | Amex Card                             | 020101                    |           | CC | Y |
|               12413 | Amex HYSA                             | 320017952413              | N         |    | N |
|               21005 | Amex Personal Loan                    | 020302                    | N         |    | N |
|               11005 | Amex Rewards Checking                 | 400213999511              | N         |    | N |
|               28461 | Apple Card -- Default                 | ....8461                  | N         | CC | Y |
|               15957 | Apple Card Cash                       | 010101                    | N         |  ??  | Y |
|               19986 | Apple Cash                            | 10101                     | N         |  CA  | Y |
|               19999 | Apple Installment                     | 020302                    | N         |  ??  | Y |
|               25957 | Apple m/c - Virtual                   | 020101                    |           |  ??  | Y |
|               28538 | Apple m/c- ApplePay                   | *****8538                 | N         |  CC  | Y |
|               27235 | Apple Titanium Card OLD               | 020101                    | N         |  CC  | Y |
|               23351 | Apple Titanium M/C                    | ****3351                  | N         |  CC  | Y |
|               28023 | BofA Visa                             | 020101                    | N         |  CC  | Y |
|               17452 | Capital One 360 Check                 | 4684-9010                 | N         |  DB  | Y |
|    s/b 10207?  19970 | Capital One Debit                     | 010101                    | N         | CH | Y |
|               17114 | Capital One Perf Sav                  | 010101                    | N         | SA | Y |
|               26993 | Capital One Quicksilver               | 020101                    | N         |  CC  | Y |
|               11416 | Further Value HSA                     | SA3108130                 | N         |    | N |
|               21416 | Further Visa                          | 010101                    | N         |    | N |
|               12505 | HealthEquityDebit                     | *****2505                 | N         |  DB  | Y |
|               42102 | Interest Income                       | 040102                    | N         |  ??  | Y |
|               25598 | MGM Rewards MC                        | 020101                    | N         |    | N |
|            ??   69999 | MN Tax Refund                         | 060101                    | N         |  ??  | Y |
|            ??   60101 | Other Revenue                         | 060101                    | N         |  ??  | Y |
|            ??   42202 | Pension Income                        | 040202                    | N         |  ??  | Y |
|               19998 | Petty Cash                            | 010101                    | N         | CA   | Y |
|               22301 | REI - Capital One                     | 020101                    |           |  CC  | Y |
|               19091 | Schwab Contributory IRA               | 1595-9091                 | N         | IR | Y |
|               19997 | Schwab Govt Money Inv                 | SCHWABGMI                 | N         | IR   | Y |
|               13897 | Schwab Inherited IRA                  | 2646-3897                 | N         | IR | Y |
|               15782 | Schwab One **Debit**                           | 4684-9010                 | N         | DB | Y |
|               16935 | Schwab One Cash Account ??                            | 8391-6935                 | N         | ?? | Y |
|               13031 | Simple Abundance Eq                   | 010101                    | N         |    | N |
|               42133 | Strategic Portfolio Service Advantage | 010104                    | Q         |    | N |
|               45133 | Strategic Portfolio Service Advantage | 010104                    | Q         |    | N |
|               46133 | Strategic Portfolio Service Advantage | 010104                    | N         |    | N |
|               13415 | Target Debit Card                     | 010101                    | N         |    | N |
|               18315 | Transamerica NQDC                     | NQ98315 00001 NQDC        | N         |    | N |
|               12923 | Transamerica QK62                     | QK62923 00001 401(k) Plan | Q         |    | N |
|               86195 | USB Fees                              | 060311                    | N         |    | N |
|               16195 | USB Savings                           | 010101                    | N         |    | N |
|               96195 | USB Savings Int Paid                  | 010101                    | N         |    | N |
|           ??    40102 | W2 Income                             | 040102                    | N         |    | N |
|           ??    41102 | W2 Income                             | 040102                    | N         |    | N |

State sql files for theses changes in

```
MyFinance
  |
  + db
    |
    + scripts
      |
      + 01_recreate_finance_tst.sql
      + 02_load_finance_tst.sql
      ...
```    