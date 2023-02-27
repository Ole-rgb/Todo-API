#This file is responsible for signing. encoding, decoding and returning JWTs
import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#this function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "accessToken": token
    }

#function used for signing the JWT string
def signJWT(username: str):
    payload = {
        "username": username, #something unique
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET,  algorithm=JWT_ALGORITHM)
    return token_response(token)

#function decodes the token and returns it, if it isnt expired!
def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token,JWT_SECRET, JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}