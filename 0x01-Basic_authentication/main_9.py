#!/usr/bin/env python3
""" Test extract_user_credentials method of BasicAuth
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_user_credentials(None))  # (None, None)
print(a.extract_user_credentials(89))  # (None, None)
print(a.extract_user_credentials("Holberton School"))  # (None, None)
print(a.extract_user_credentials("Holberton:School"))  # ('Holberton', 'School')

# ('bob@gmail.com', 'toto1234')
print(a.extract_user_credentials("bob@gmail.com:toto1234"))
