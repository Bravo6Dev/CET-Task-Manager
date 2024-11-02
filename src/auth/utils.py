from logging import exception
from passlib.context import CryptContext
import jwt

from src.config import config
from datetime import datetime, timedelta

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)

def create_token(user_data:dict, time_delta = None) -> str:
    payload = {}
    payload['data'] = user_data
    payload['exp'] = datetime.now() + time_delta if time_delta else datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm=config.ALGORITHM)
    return token

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except jwt.PyJWTError as e:
        exception(e)
        return None

def verfiy_password (password: str, hashed_password: str) -> bool:
    return context.verify(password, hashed_password)


