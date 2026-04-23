DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM finance_tst.external_accounts WHERE external_account_id = 10207) THEN
    RAISE NOTICE 'External account 10207 exists.';
  ELSE
    RAISE NOTICE 'External account 10207 does not exist...creating';
    INSERT INTO finance_tst.external_accounts
    (
        external_account_id,
        account_name,
        account_number,
        qualified,
        account_type,
        active
    )
    VALUES
    (
        10207,
        'Capital One Debit',
        '*****0207',
        'N',
        'DB',
        TRUE
    );
  END IF;
  
  IF EXISTS (
    SELECT 1
    FROM finance_tst.voucher
    WHERE payment_source_id = 19970
      AND payment_type_id =10
  ) THEN
        RAISE NOTICE'Updating existing vouchers';
        UPDATE finance_tst.voucher
        SET payment_source_id=10207
        WHERE payment_source_id = 19970
          AND payment_type_id =10;
    ELSE
        RAISE NOTICE'No vouchers found matching the criteria';
    END IF;
END $$;