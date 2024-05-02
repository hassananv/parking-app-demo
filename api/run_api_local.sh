#!/bin/bash
echo "___Run Api Locally___"

source .env

alembic upgrade head

uvicorn app:app --reload --port=8080