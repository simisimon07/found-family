# Deployment Configuration Guide

## Problem Fixed
The original error was caused by Python 3.14 compatibility issues with the `protobuf` library used by `google-generativeai`. The solution pins Python to version 3.11, which is stable and well-tested.

## Files Created

### 1. `runtime.txt` (Render)
Specifies Python 3.11 for Render deployment. Render reads this file to determine which Python version to use.

### 2. `render.yaml` (Render)
Infrastructure configuration file for Render. Define your service settings here including environment variables.

### 3. `vercel.json` (Vercel)
Configuration file for Vercel deployment. Specifies how to build and deploy your Flask app.

### 4. `wsgi.py` (Vercel)
WSGI entry point required by Vercel's Python runtime. This is the main entry file for serverless deployment.

### 5. `build.sh` (Vercel)
Custom build script for Vercel to install dependencies and initialize the database.

### 6. Updated `requirements.txt`
- Updated `google-generativeai` from 0.3.0 to 0.7.1 (compatible with Python 3.11)
- Pinned `protobuf` to 4.25.3 (Python 3.14 compatible version)
- Added `google-api-core` for protobuf support
- Updated to ensure all dependencies work together

### 7. Updated `app.py`
Modified the Flask app startup to use environment variables for PORT, allowing it to work correctly on both platforms.

## Deployment Steps

### For Render:
1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect `runtime.txt` and `render.yaml`
5. Set environment variables in Render dashboard (DATABASE_URL, GOOGLE_API_KEY, etc.)

### For Vercel:
1. Install Vercel CLI: `npm install -g vercel`
2. Run: `vercel` in your project directory
3. Vercel will read `vercel.json` for configuration
4. Set environment variables in Vercel dashboard
5. Deploy with: `vercel --prod`

## Environment Variables Needed
Both platforms need these variables set:
- `GOOGLE_API_KEY` - Your Google Generative AI API key
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)
- `FLASK_ENV` - Set to "production" for live deployment

## Key Changes Made
1. **Python Version**: Downgraded from 3.14 (incompatible) to 3.11 (stable)
2. **Dependencies**: Updated for Python 3.11 compatibility
3. **Port Configuration**: Now uses PORT environment variable (required for Render/Vercel)
4. **WSGI Support**: Added wsgi.py for serverless deployment

## Testing Locally
```bash
pip install -r requirements.txt
export FLASK_ENV=development
python app.py
```

## Troubleshooting
- If you still get protobuf errors, clear your pip cache: `pip cache purge`
- Make sure Python version is 3.11 locally: `python --version`
- Check environment variables are set: `echo $GOOGLE_API_KEY`
