# Release notes for MyFinance Release 2.0

1. Added entry in .env INSTANCE  = ''  This text will be displayed in the Nav bar indicating which instance you are viewing, such as *ESC-Sandbox:Test*.  eskoviak/issue-28

    SCHEMA:  No  
    CODE:  Yes  
    CSS:  Yes 

2. Limit payment source based on payment type.  eskoviak/issue-30

    SCHEMA:  Yes

        (update_release_2.sql)
        
        -Extend length of external_accounts.account_type
        -Add new table pmt_type_pmt_src_xref
