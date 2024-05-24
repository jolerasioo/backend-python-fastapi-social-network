from pydantic_settings import BaseSettings



# environment settings for the app
class Settings(BaseSettings):
    '''settings for the app'''
    secret_key: str
    algorithm: str 
    access_token_expire_minutes: int
    # postgresql database url constructor
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    class Config:
        '''config for the settings'''
        env_file = ".env"

settings = Settings()