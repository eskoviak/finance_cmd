-- Active: 1660319329194@@127.0.0.1@5432@finance@finance
CREATE OR REPLACE FUNCTION finance.search_vendor(character varying) 
RETURNS TABLE (
    vendor_number integer,
    vendor_short_desc varchar(30)
)
AS $$
    select vendor_number, vendor_short_desc from finance.vendors where vendor_short_desc ILIKE ('%' || $1 || '%');
$$ LANGUAGE SQL; 