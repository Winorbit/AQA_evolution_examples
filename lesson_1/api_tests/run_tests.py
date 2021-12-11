from api_tests import TestUsers

if __name__ == '__main__':
	TestUsers().test_create_user()
	TestUsers().test_create_user_invalid_data()