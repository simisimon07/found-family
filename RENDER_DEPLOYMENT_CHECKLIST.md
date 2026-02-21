Render Deployment Checklist

1. Confirm Python runtime
   - Include `runtime.txt` with `python-3.11.8` at project root.

2. Requirements
   - `requirements.txt` pinned and includes `gunicorn` and compatible `protobuf`:
     - google-generativeai==0.7.1
     - protobuf==4.25.3
     - google-api-core==2.13.0
     - gunicorn==20.1.0

3. Start command
   - Render will use `Procfile`: `web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 3`

4. Environment variables (set in Render dashboard)
   - `GEMINI_API_KEY` or `GOOGLE_API_KEY` (required)
   - `SECRET_KEY` (required)
   - `DATABASE_URL` (optional; use managed DB in prod)
   - `FLASK_ENV=production`

5. Security & best practices
   - Do NOT commit real `.env` to repo; use Render secrets.
   - Use managed DB credentials in `DATABASE_URL` (Postgres recommended).
   - Ensure application logs do not print secrets.

6. Health checks
   - Use `/api/health` endpoint for readiness checks.

7. Deployment steps
   - Push branch to GitHub
   - Create a new Web Service on Render and connect the repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 3`
   - Add required environment variables in the Render dashboard

8. Troubleshooting
   - If you see protobuf import errors, confirm Render is using Python 3.11 (check logs)
   - Clear virtualenv / rebuild if dependency pins change

9. Optional
   - Use a process manager or add autoscaling in Render settings for production traffic
