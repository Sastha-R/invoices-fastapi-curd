import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env")
    db_host : str
    db_name : str
    db_user : str
    db_password : str
    db_port :int 


setting = Settings()