SELECT v.voucher_date
  ,v.voucher_number AS VoucherNo
  ,ve.vendor_short_desc AS Vendor
  ,v.voucher_amt
  ,e.account_name
  ,vd.id as DetailID
  ,vd.account_number
  ,vd.split_seq_number
  ,vd.amount
  ,vd.dimension_1
  ,vd.dimension_2
FROM finance.voucher v
JOIN finance.voucher_detail vd on v.voucher_number = vd.voucher_number
JOIN finance.vendors ve on v.vendor_number = ve.vendor_number
JOIN finance.external_accounts e on v.payment_source_id = e.external_account_id
WHERE
	voucher_date > '5/12/24'
-- v.voucher_number > 2145
-- v.vendor_number = (select vendor_number from vendors where vendor_short_desc ilike '%keller%')
  --AND voucher_date > '12/1/22'
--WHERE account_number IN (
--  SELECT DISTINCT account_number FROM finance.voucher_detail
--)
ORDER by voucher_date, split_seq_number
