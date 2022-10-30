import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
import json
import pg_utils

print(json.dumps(pg_utils.get_voucher(1200)))
