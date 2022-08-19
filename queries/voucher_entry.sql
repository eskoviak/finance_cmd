-- Active: 1660319329194@@127.0.0.1@5432@finance@public
select finance.insert_voucher('8/17/22 12:30 CDT','',35,2,2003,4,19998,'Red Wing, MN');

select finance.insert_voucher_detail(1088,1,'050101',35,'Haircut','','29 plus 6 tip');
