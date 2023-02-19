-- Active: 1660319329194@@127.0.0.1@5432@finance
set search_path = 'finance';
select id
  ,invoice_id
  ,v.vendor_short_desc
  ,stmt_dt
  ,stmt_amt
  ,payment_due_dt
  ,e.account_name as Source
  ,payment_voucher_id
from accounts_payable ap
join vendors v on ap.vendor_number = v.vendor_number
join external_accounts e on ap.payment_source_id = e.external_account_id
where payment_due_dt between '2/17/23' and '3/3/23'
  and payment_voucher_id is NULL
order by payment_due_dt;

select sum(stmt_amt) AS Total
from accounts_payable
where payment_due_dt between '2/17/23' and '3/3/23'
  and payment_voucher_id is NULL;