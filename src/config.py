from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    '''
    This class for python config to connect with .env file 
    .env file include secret and important data
    model_config is an instance from 'SettingsConfigDict' that hold where .env file is exist
    every attribute or key in .env file must have an property in this class
    '''
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )

config = Settings()