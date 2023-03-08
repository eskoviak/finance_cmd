
--declare @voucher_id = INTEGER
--declare @stmt_amt = FLOAT
--declare @id = INTEGER
--set @voucher_id = 1517
--set @stmt_amt = 1852.88
--set @id = 27

--with (vn, sa, ai) as (values (1517, 1852.88, 27))


update accounts_payable
set payment_voucher_id = 1517,
stmt_amt = 1852.88
where id = 27;