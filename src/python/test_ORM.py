import sys

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from models_tst import (ExternalAccounts, PaymentType, Vendors, Voucher,
                        VoucherType)

engine = create_engine("postgresql://postgres:terces##@localhost:5432/finance")
with Session(engine) as session:
    results = session.execute(select(Voucher).where(Voucher.voucher_number == 100))
    for row in results:
        

        print(row)

