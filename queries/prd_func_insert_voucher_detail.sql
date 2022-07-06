CREATE OR REPLACE FUNCTION finance.insert_voucher_detail(integer, integer, character varying, numeric, character varying, character varying, text)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
    voucher_number ALIAS for $1;
    split_seq_number ALIAS for $2;
    account_number ALIAS for $3;
    amount ALIAS for $4;
    dimension_1 ALIAS for $5;
    dimension_2 ALIAS for $6;
    memo ALIAS for $7;
BEGIN
    INSERT INTO finance.voucher_detail(id,voucher_number,split_seq_number,account_number,amount,dimension_1,dimension_2,memo)
    VALUES (
        nextval('finance.voucher_detail_id_seq'),
	voucher_number,
        split_seq_number,
        account_number,
        amount,
        dimension_1,
	dimension_2,
        memo
    );

    RETURN currval('finance.voucher_detail_id_seq');

END;
$function$
