import os
import datetime
import jwt

SECRET_KEY="f1c0a633-3310-4593-b4e0-2e60174ecac1"

# generates a to with user id in payload
def genrateToken(userid):
    token=jwt.encode({"user":userid,"exp":datetime.datetime.now()+datetime.timedelta(minutes=30)},key=SECRET_KEY, algorithm="HS512")
    return token

# verify user token and return the payload data
def verify_(token):
    try:
        data=jwt.decode(token,key=SECRET_KEY, algorithm="HS512")
        print(data)
        return data
    except Exception as e:
        return f"Invalid token...{e}"