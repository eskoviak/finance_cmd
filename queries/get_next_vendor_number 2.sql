SELECT MAX(vendor_number)+1
FROM vendors
WHERE vendor_number BETWEEN 1000 AND 1999;
