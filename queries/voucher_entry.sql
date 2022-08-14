-- Active: 1660319329194@@127.0.0.1@5432@finance@public
select finance.insert_voucher('8/13/22 09:56 CDT','',38.43,2,2000,6,27235,'Red Wing, MN');

select finance.insert_voucher_detail(1081,3,'050101',18.08,'Grocery','','');
