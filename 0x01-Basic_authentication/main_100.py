#!/usr/bin/env python3
""" Tests the improved <extract_user_credentials> method of class BasicAuth
"""
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# Create a user test
user_email = "bob100@hbtn.io"
user_clear_pwd = "H0lberton:School:98!"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {}".format(user.id))
user.save()

# Create second user with multiple ':' characters
user2_email = "alfred@hbtn.io"
user2_clear_pwd = "H0lberton:School:is:cool!"

user2 = User()
user2.email = user2_email
user2.password = user2_clear_pwd
print("New user: {}".format(user2.id))
user2.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(
    basic_clear.encode('utf-8')).decode("utf-8")))

basic_clear2 = "{}:{}".format(user2_email, user2_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(
    basic_clear2.encode('utf-8')).decode("utf-8")))
