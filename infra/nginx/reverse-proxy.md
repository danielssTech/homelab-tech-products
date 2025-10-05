Nginx Reverse Proxy – TechProducts

This document describes the Nginx configuration that serves static files and acts as a reverse proxy for the FastAPI backend.

Objective

Expose only port 80 externally. Serve the static frontend (static_site/) from Nginx. Proxy traffic from /api/ to the internal FastAPI app (port :8000). Keep logs and configuration ready to reproduce on any host.

Structure
infra/nginx/
├─ techProducts.conf              # Server blocks (HTTP + reverse proxy)
├─ log_format_techproducts.conf   # Optional custom log format
└─ reverse-proxy.md               # This document
static_site/
├─ index.html
└─ js/app.js

Upstream and Virtual Hosts

Note: Adjust the upstream IP if your app does not run on that address.
In this project, the app runs at 192.168.133.1:8000.

# --- upstream (backend FastAPI) ---
upstream project1_app {
    server 192.168.133.1:8000;
    keepalive 16;
}

# --- HTTP only (no TLS) ---
server {
    listen 80;
    server_name _;

    # Static files: adjust to the actual deployment path
    # Typically: /var/www/techProducts/html
    root /var/www/techProducts/html;
    index index.html;

    # Basic security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self' 'unsafe-inline'" always;

    # API → FastAPI
    location /api/ {
        proxy_pass         http://project1_app;   # ← no trailing slash to keep /api prefix
        proxy_http_version 1.1;

        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;

        # Uncomment only if you’ll use WebSockets
        # proxy_set_header   Upgrade           $http_upgrade;
        # proxy_set_header   Connection        "upgrade";

        proxy_connect_timeout 5s;
        proxy_read_timeout    60s;
        proxy_send_timeout    60s;
    }

    # Static files (index.html + /js/app.js)
    location = / { try_files $uri /index.html; }
    location /  { try_files $uri $uri/ /index.html; expires 10m; }
}

Static Deployment Path
    Repository: static_site/
    Nginx root on server: /var/www/techProducts/html

    Deploy:
    sudo mkdir -p /var/www/techProducts/html
    sudo cp -r static_site/* /var/www/techProducts/html/

Useful Commands
    sudo nginx -t                                   # Test syntax
    sudo systemctl reload nginx                     # Reload configuration
    curl -i http://192.168.133.1:8000/api/health    # backend reachability
    curl -i http://localhost/api/health             # through Nginx

Healthcheck
    Endpoint: GET /api/health
    Expected Response: 200 OK with:
    {"status":"ok","db":"up"}

Quick Troubleshooting
502 Bad Gateway
    FastAPI app not running at 192.168.133.1:8000
    Firewall or network issue between Nginx and the app
    Wrong proxy_pass target (IP/port mismatch)

404 on static files
    root does not match the actual path
    index.html or /js/app.js missing in the Nginx root directory

HTML/JS not rendering
    Ensure <script src="/js/app.js" defer></script> exists
    Verify js/app.js is under /var/www/techProducts/html/js/

Minimal Security Checklist
 Only Ngimx exposes port 80 (App and DB not publicly exposed)
 Basic security headers added (X-Content-Type-Options, etc.)
 Secrets stored outside the repository
 Backup and restore successfully tested (see Runbook)