
from fastapi import FastAPI

import uvicorn
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from core.config import settings
from core.multi_database_middleware import DATABASE_URL

from oidc.oidc_router import router as oidc_router
from api.api import router as api_router

from starlette.middleware.sessions import SessionMiddleware


#___________________________________________________

def get_application() -> FastAPI:
   
    new_app = FastAPI(
        title=settings.API_TITLE, 
        description=settings.API_DESCRIPTION, 
        version=settings.API_VERSION
    )
    print("====CORES=====")
    print(settings.CORS_ORIGIN)
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    new_app.add_middleware(SessionMiddleware, secret_key="store secret key")
    new_app.include_router(oidc_router)
    new_app.include_router(api_router)


    new_app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

    return new_app



app = get_application()

@app.get('/api/v1/health')
def openshift_Health_Check():
    print("______Health check for OpenShift______")
    return "Healthy"  
     


def start_main():
    
    print("____FAST_API____")
    print("API_HTTP_PORT is: ",os.getenv('API_HTTP_PORT', ''))
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    start_main()