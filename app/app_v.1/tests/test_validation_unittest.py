import os
import sys
import unittest

p = os.path.abspath('.')
sys.path.insert(1, p)

from api.validation import check_email

class TestEmailValidation(unittest.TestCase):

	def test_validate_valid_email(self):
		valid_email = "myemail@gmail.com"
		self.assertTrue(check_email(valid_email))

	def test_validate_invalid_email(self):
		invalid_email_1 = "myemail"
		invalid_email_2 = "myemail.com"
		self.assertFalse(check_email(invalid_email_1))
		self.assertFalse(check_email(invalid_email_2))

if __name__ == '__main__':
	unittest.main()