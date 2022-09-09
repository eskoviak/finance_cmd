-- Active: 1660319329194@@127.0.0.1@5432@finance@public
select finance.insert_voucher('9/8/22 16:31 CDT','',43.89,2,2000,6,26624,'Red Wing, MN');

select finance.insert_voucher_detail(1135,2,'050101',6.48,'Grocery','','');
