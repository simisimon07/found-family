#!/bin/bash
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create database
python -c "from app import app; 
with app.app_context(): 
    from models import db; 
    db.create_all()"
