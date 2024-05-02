import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_SERVICE_NAME:str = os.getenv('DATABASE_SERVICE_NAME','db')
    DATABASE_ENGINE:str = os.getenv('DATABASE_ENGINE','postgresql')
    DATABASE_NAME:str = os.getenv('DATABASE_NAME','your_db_name')
    DATABASE_USER:str = os.getenv('DATABASE_USER','your_db_user')
    DATABASE_PASSWORD:str = os.getenv('DATABASE_PASSWORD','your_db_password')
    DB_SERVICE_HOST:str = os.getenv('DB_SERVICE_HOST','localhost')
    DB_SERVICE_PORT:str = os.getenv('DB_SERVICE_PORT','5433')

    FRONTEND_HOST_URL:str = os.getenv('FRONTEND_HOST_URL','http://localhost:8081')
    DEFAULT_BASE_URL:str = os.getenv('DEFAULT_BASE_URL' ,'/parking-app')
    URL_SCHEME:str = os.getenv('URL_SCHEME' ,'http')
    APP_RUN_IN_DOCKER:str = os.getenv('APP_RUN_IN_DOCKER', 'False')
    
    JWT_SECRET_KEY:str = os.getenv('JWT_SECRET_KEY','please-pass-your-secrets-in-a-secure-manner')
    DATA_SECURITY_KEY:str = os.getenv('DATA_SECURITY_KEY','secrets-can-be-included-as-openshift-private-secrets')
    
    OIDC_RP_PROVIDER_URL:str = os.getenv('OIDC_RP_PROVIDER_URL')
    OIDC_RP_PROVIDER_REALM :str= os.getenv('OIDC_RP_PROVIDER_REALM')
    OIDC_RP_CLIENT_ID:str = os.getenv('OIDC_RP_CLIENT_ID')
    OIDC_RP_CLIENT_SECRET:str = os.getenv('OIDC_RP_CLIENT_SECRET')
    OIDC_RP_KC_IDP_HINT:str = os.getenv('OIDC_RP_KC_IDP_HINT')


    # # API
    API_PREFIX:str = os.getenv('API_PREFIX', '/api/v1')
    API_VERSION:str = '0.1.0'
    API_TITLE:str = 'Parking Reservation Application API'
    API_DESCRIPTION:str = API_TITLE
   

    # # cors
    CORS_ORIGIN:list = str(os.getenv('CORS_ORIGIN', '*')).split(',')    


    class Config:
        case_sensitive = True


settings = Settings()
