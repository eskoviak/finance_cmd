-- Active: 1660319329194@@127.0.0.1@5432@finance@public
select finance.insert_voucher('9/13/22 15:50 CDT','',14.09,2,1002,4,19998,'Red Wing, MN');

select finance.insert_voucher_detail(1142,1,'050101',14.09,'Grocery','','');
