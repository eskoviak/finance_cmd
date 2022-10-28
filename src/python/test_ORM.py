from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
from models_tst import Vendors

engine = create_engine("postgresql://postgres:terces##@localhost:5432/finance")
with Session(engine) as session:
    results = session.execute(select(Vendors))
    print(results)

