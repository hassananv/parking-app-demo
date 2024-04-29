#!/bin/bash
echo "___Run Api Locally___"

alembic upgrade head

uvicorn app:app --reload --port=8080