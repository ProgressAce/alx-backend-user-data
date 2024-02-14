#!/usr/bin/env python3
""" Test user_object_from_credentials method of BasicAuth
"""
import uuid
import os
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# WARNING: this test removes the existing User database
auth1 = BasicAuth()
os.remove('.db_User.json')
u = auth1.user_object_from_credentials('abacus21@gmail.com', 'Hopping^65')
print(f"database with no existing user object: {u}")  # None
# WARNING END

""" Create a user test """
user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Bob"
user.last_name = "Dylan"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()

""" Retreive this user via the class BasicAuth """

a = BasicAuth()

u = a.user_object_from_credentials(None, None)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(89, 98)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials("email@notfound.com", "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, user_clear_pwd)
print(u.display_name() if u is not None else "None")
