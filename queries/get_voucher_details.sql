SELECT v.voucher_date
  ,v.voucher_number
  ,(SELECT vendor_short_desc FROM finance.vendors WHERE vendor_number = v.vendor_number)
  ,vd.account_number
  ,vd.split_seq_number
  ,vd.dimension_1
  ,vd.dimension_2
FROM finance.voucher v
JOIN finance.voucher_detail vd on v.voucher_number = vd.voucher_number
WHERE account_number IN (
  SELECT DISTINCT account_number FROM finance.voucher_detail
)
ORDER by voucher_date, split_seq_number
