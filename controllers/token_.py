import os
import datetime
# from jose import JWTError, jwt
import jwt


# load_dotenv()
SECRET_KEY="f1c0a633-3310-4593-b4e0-2e60174ecac1"

def genrateToken(userid):
    token=jwt.encode({"user":userid,"exp":datetime.datetime.now()+datetime.timedelta(minutes=30)},SECRET_KEY)
    return token

def verify_(token):
    try:
        data=jwt.decode(token,SECRET_KEY)
        return data
    except:
        return "Invalid token..."