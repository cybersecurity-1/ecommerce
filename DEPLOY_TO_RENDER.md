# Deploy to Render — quick steps

This repository contains the Django app under `project1/website1`.

Follow these steps to deploy on Render (recommended):

1. Push your repository to GitHub (already done).

2. In Render dashboard, create a new **Web Service** and connect your GitHub repo.
   - Branch: `main`
   - Environment: `Python 3`
   - Build command: `pip install -r project1/website1/requirements.txt`
   - Start command: `gunicorn website1.wsgi:application --chdir project1/website1 --bind 0.0.0.0:$PORT`

3. Add environment variables in the Render Service settings:
   - `SECRET_KEY`: (set a long random value) — mark as secret/private
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app.onrender.com` (or comma-separated hosts)

4. (Recommended) Create a managed PostgreSQL database in Render and copy the `DATABASE_URL` value into your Web Service environment variables.

5. Ensure static files are collected and migrations run. You can add a deploy hook in the Render UI or run manually in the instance shell:
   ```bash
   python project1/website1/manage.py migrate
   python project1/website1/manage.py collectstatic --noinput
   ```

6. If your app uses media uploads, configure S3 or another external storage — Render's filesystem is ephemeral.

Notes
- `render.yaml` is included for convenience; you can also configure via the Render web UI.
- If you run into `DisallowedHost` errors, check `ALLOWED_HOSTS` and `DEBUG`.
- If `psycopg2` build fails, ensure `psycopg2-binary` is in `requirements.txt` (already present).
