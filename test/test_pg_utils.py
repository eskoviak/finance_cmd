import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
import json
from MyFinance.utils.pg_utils import PgUtils
import unittest
from utils import config
from pathlib import Path
import os


# TODO Tests don't work with config from dotenv (false positive)
class TestPGUtils(unittest.TestCase):

    util = config.Util()

    
    def setUp(self) -> None:
        #config = self.util.get_config(os.path.abspath('/Users/edmundlskoviak/Documents/repos/finance_cmd'))
        #self.pg_utils = PgUtils(config['PGURIT'])
        self.pg_utils = PgUtils('postgresql://postgres:terces##@localhost:5432/finance')
        return super().setUp()
    
    def test_get_voucher(self):
        test_voucher_number = 133
        result = self.pg_utils.get_voucher(test_voucher_number)
        self.assertIs(type(result), dict, 'Result is not a dict')
        self.assertEqual(result['voucher_number'], test_voucher_number, 'Voucher number not matched')
    
    def test_get_vendors(self):
        result = self.pg_utils.get_vendors()
        self.assertIs(type(result), list, 'Result is not a list')
        self.assertGreater(len(result), 0, 'Reuslt set is empty')

    def test_get_external_accounts(self):
        result = self.pg_utils.get_external_accounts()
        self.assertIs(type(result), list, 'Result is not a list')
        self.assertGreater(len(result), 0, 'Reuslt set is empty')

    def test_get_voucher_types(self):
        result = self.pg_utils.get_voucher_types()
        self.assertIs(type(result), list, 'Result is not a list')
        self.assertGreater(len(result), 0, 'Result set is empty')
        
    def test_get_next_split_number(self):
        test_voucher_number = 133
        result = self.pg_utils.get_next_split_number(test_voucher_number)
        self.assertIs(type(result), int, 'Result is not an int')
        self.assertEqual(result, 2, 'Result is not equal to 3')
        result = self.pg_utils.get_next_split_number(99999)
        self.assertEqual(result, 1, 'wrong results for non existent voucher_number')

    def test_get_liability(self):
        test_liability_number = 4
        result = self.pg_utils.get_liability(test_liability_number)
        self.assertIs(type(result), dict, 'Result is not a dict')
        self.assertEqual(result['current_balance_amt'], 4480.68, 'Current balance amount not matched')

    def test_get_liability_by_account(self):
        test_account_number = 21005
        result = self.pg_utils.get_liability_by_account(test_account_number)
        self.assertIs(type(result), list, 'Result is not a list')
        self.assertEqual(len(result), 3, 'List is not 3 items long')

    

