# Test Report – /api/health Endpoint

## Objective
Verify that the health endpoint returns HTTP 200 and service status.

## Steps
1. Run the FastAPI app and ensure Nginx is active.
2. Open browser or use curl http://192.168.133.10/api/health
3. Observe the response.

## Expected Result
- HTTP Status: **200 OK**
- Response Body:
```json
{"status":"ok","db":"up"}

Conclusion: Healthcheck endpoint working correctly and reachable through Nginx reverse proxy.
