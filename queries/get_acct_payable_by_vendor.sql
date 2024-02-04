SELECT id
  ,invoice_id
  ,vendor_short_desc
  ,stmt_dt
  ,stmt_amt
  ,payment_due_dt
  ,account_name
  ,payment_voucher_id
FROM accounts_payable ap 
JOIN vendors v ON ap.vendor_number = v.vendor_number
JOIN external_accounts ea on ap.payment_source_id = ea.external_account_id
WHERE ap.vendor_number = (SELECT vendor_number FROM vendors WHERE vendor_short_desc ILIKE '%Verizon%');