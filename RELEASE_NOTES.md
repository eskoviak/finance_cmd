# Release notes for MyFinance Release 2.0

1. Added entry in .env INSTANCE  = ''  This text will be displayed in the Nav bar indicating which instance you are viewing, such as *ESC-Sandbox:Test*.  

    SCHEMA:  No  
    CODE:  Yes  
    CSS:  Yes 
    (eskoviak/issue28)

2. Limit payment source based on payment type.

    SCHEMA:  Yes

        alter table external_accounts alter column account_type type  varchar(15);
