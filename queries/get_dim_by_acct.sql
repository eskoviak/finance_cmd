-- Active: 1660319329194@@127.0.0.1@5432@finance@finance
SELECT account_number
    ,dimension_1
    ,dimension_2
from finance.voucher_detail
ORDER BY account_number;