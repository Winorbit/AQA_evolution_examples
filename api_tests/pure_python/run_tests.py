from api_tests import TestUsers

import argparse

parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('--tests', dest='tests', type=str, help='Type of test')


if __name__ == '__main__':
	args = parser.parse_args()
	if args:
		if args.tests == "users":
			TestUsers().test_create_user()
			TestUsers().test_update_user()

			TestUsers().test_create_user_invalid_data()
			TestUsers().test_update_user_invalid_data()