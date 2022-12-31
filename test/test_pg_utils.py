import sys
sys.path.append('/Users/edmundlskoviak/Documents/repos/finance_cmd')
import json
from MyFinance.utils.pg_utils import PgUtils
import unittest

# TODO Tests don't work with config from dotenv (false positive)
class TestPGUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.pg_utils = PgUtils()
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
        self.assertEqual(result, 3, 'Result is not equal to 3')
        result = self.pg_utils.get_next_split_number(99999)
        self.assertEqual(result, 1, 'wrong results for non existent voucher_number')

    

