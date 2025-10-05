# Runbook – Deploy & Restore
## Deploy
1. Clone repo
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Nginx reverse proxy points to the internal FastAPI app (`192.168.133.1:8000`) defined in:
    upstream project1_app {
        server 192.168.133.1:8000;
    }
    location /api/ {
        proxy_pass http://project1_app;
    }

## Healthchecks
- `GET /api/health` → 200 OK

## Backup
- `pg_dump -h <host> -U <user> -d <db> -Fc > backups/techproducts_$(date +%F_%H-%M).dump`

## Restore
- `pg_restore -h <host> -U <user> -d <db> -c backups/techproducts_2025-10-04_15-56.dump`
