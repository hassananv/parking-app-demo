import os
from pydantic import BaseSettings


class Settings(BaseSettings):

    DATABASE_SERVICE_NAME = os.getenv('DATABASE_SERVICE_NAME','db')
    DATABASE_ENGINE = os.getenv('DATABASE_ENGINE','postgresql')
    DATABASE_NAME = os.getenv('DATABASE_NAME','your_db_name')
    DATABASE_USER = os.getenv('DATABASE_USER','your_db_user')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD','your_db_password')
    DB_SERVICE_HOST = os.getenv('DB_SERVICE_HOST','localhost')
    DB_SERVICE_PORT = os.getenv('DB_SERVICE_PORT','5433')

    FRONTEND_HOST_URL = os.getenv('FRONTEND_HOST_URL','http://localhost:8081')
    DEFAULT_BASE_URL = os.getenv('DEFAULT_BASE_URL' ,'/parking-app')
    URL_SCHEME = os.getenv('URL_SCHEME' ,'http')
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY','please-pass-your-secrets-in-a-secure-manner')
    DATA_SECURITY_KEY = os.getenv('DATA_SECURITY_KEY','secrets-can-be-included-as-openshift-private-secrets')
    

    # # API
    API_PREFIX = os.getenv('API_PREFIX', '/api/v1')
    API_VERSION = '0.1.0'
    API_TITLE = 'Parking Reservation Application API'
    API_DESCRIPTION = API_TITLE
   

    # # cors
    CORS_ORIGIN = str(os.getenv('CORS_ORIGIN', '*')).split(',')    


    class Config:
        case_sensitive = True


settings = Settings()
