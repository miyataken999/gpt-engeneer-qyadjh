#!/bin/bash

# Install dependencies
python -m pip install -r requirements.txt

# Run the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000 &
