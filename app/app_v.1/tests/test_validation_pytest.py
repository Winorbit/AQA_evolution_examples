import os
import sys
import pytest

p = os.path.abspath('.')
sys.path.insert(1, p)

from api.validation import check_email

def test_validate_valid_email(self):
	valid_email = "myemail@gmail.com"
	assert True == check_email(valid_email)

def test_validate_invalid_email(self):
	invalid_email_1 = "myemail"
	invalid_email_2 = "myemail.com"
	assert False == check_email(invalid_email_1)
	assert False == check_email(invalid_email_2)

