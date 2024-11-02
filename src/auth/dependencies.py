from fastapi.security import HTTPBearer
from fastapi import Request, Depends, HTTPException, status
from logging import exception

from src.auth.utils import decode_token

from src.Members.sql_model import members

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db_context import get_session
from src.Members.service import MemeberService

service = MemeberService()

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        Initialize an AccessTokenBearer instance.

        Args:
            auto_error (bool): Whether to automatically raise an exception if the
                authentication fails. Defaults to True.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        """
        Validate the access token.

        Args:
            request: The request to validate.

        Returns:
            The decoded token data if the token is valid, otherwise raises an HTTPException.
        """
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
        creds = await super().__call__(request)
        token = creds.credentials
        
        token_data = decode_token(token)
        if not self.verfiy_token(token):
            raise credentials_exception
        return token_data


    def  verfiy_token(self, token: str) -> bool:
        """
        Verify the access token.

        Args:
            token (str): The access token to verify.

        Returns:
            bool: True if the token is valid, otherwise False.
        """
        try:
            token_data = decode_token(token)
            return token_data is not None
        except Exception as ex:
            exception(ex)
            return None


async def get_current_user(token: dict = Depends(AccessTokenBearer()), 
                    session : AsyncSession = Depends(get_session)) -> members:
    try:
        user_name = token['data']['username']
        user = await service.get_member_by_username(user_name, session)
        print(user)
        return user
    except Exception as ex:
        raise ex
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

class RolesChecker:
    def __init__(self, roles: list):
        self.roles = roles

    def __call__(self, user_details : members = Depends(get_current_user)):
        print(user_details)
        The_Role = user_details.membership.Name

        if The_Role in self.roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")