SELECT voucher_date
  ,(SELECT vendor_short_desc FROM finance.vendors WHERE vendor_number = v.vendor_number)
  ,account_number
  ,dimension_1
  ,dimension_2
FROM voucher v
JOIN finance.voucher_detail vd on v.voucher_number = vd.voucher_number
WHERE account_number = '050103'
ORDER by vendor_short_desc, voucher_date
