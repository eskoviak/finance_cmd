-- Active: 1660319329194@@127.0.0.1@5432@finance@public
select finance.insert_voucher('8/28/22 13:50 CDT','',52.69,1,3016,6,28538,'Bloomington, MN');

select finance.insert_voucher_detail(1116,1,'050101',52.69,'Electronics','','');
