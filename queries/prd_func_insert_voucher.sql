CREATE OR REPLACE FUNCTION finance.insert_voucher(timestamp with time zone, character varying, numeric, integer, integer, integer, integer, character varying)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
    voucher_date ALIAS for $1;
    voucher_ref ALIAS for $2;
    voucher_amt ALIAS for $3;
    voucher_type ALIAS for $4;
    vendor_number ALIAS for $5;
    payment_type_id ALIAS for $6;
    payment_source_id ALIAS for $7;
    payment_ref ALIAS for $8;
BEGIN
    INSERT INTO finance.voucher (voucher_number, voucher_date, voucher_ref, voucher_amt, voucher_type_id, vendor_number, payment_type_id, payment_source_id, payment_ref)
    VALUES (
        nextval('finance.voucher_voucher_number_seq'),
	voucher_date,
        voucher_ref,
        voucher_amt,
        voucher_type,
        vendor_number,
        payment_type_id,
        payment_source_id,
	payment_ref
    );

    RETURN currval('finance.voucher_voucher_number_seq');

END;
$function$
