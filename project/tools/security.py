import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import request, current_app
from flask_restx import abort
from typing import Union

from coursework_3_source.project.config import BaseConfig
from coursework_3_source.project.constants import JWT_SECRET, JWT_ALGORITM
from coursework_3_source.project.exceptions import ItemNotFound


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=BaseConfig.PWD_HASH_SALT,
        iterations=BaseConfig.PWD_HASH_ITERATIONS,
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITM)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITM)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def compare_passwords(password_hash: Union[str, bytes], password: str):
    return hmac.compare_digest(
        base64.b64decode(password_hash), __generate_password_digest(password))


def login_user(req_json, user):
    user_email = req_json.get("email")
    user_pass = req_json.get("password")
    if user_email and user_pass:
        pass_hashed = user["password"]
        req_json["role"] = user["role"]
        req_json["id"] = user["id"]
        if compare_passwords(pass_hashed, user_pass):
            return generate_token(req_json)
    raise ItemNotFound


def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    raise ItemNotFound


def auth_check():
    if "Authorization" not in request.headers:
        return False
    token = request.headers["Authorization"].split("Bearer ")[-1]
    return jwt_decode(token)


def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET, JWT_ALGORITM)
    except:
        return False
    else:
        return decoded_jwt


def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization Error")

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get("role")
            if role == "admin":
                return func(*args, **kwargs)
        abort(401, "Admin role required")

    return wrapper
