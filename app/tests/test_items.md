# Test Report – /api/items Endpoint

## Objective
Validate that the `/api/items` endpoint lists items correctly.

## Steps
1. Send a GET request:
curl http://192.168.133.10/api/products_get
2. Observe the response.

## Expected Result
- HTTP Status: **200 OK**
- JSON structure similar to:
```json
[{"id":1,"name":"Router WiFi 6"},{"id":2,"name":"SSD NVMe 1TB"},{"id":13,"name":"TV"},{"id":14,"name":"Smart Speaker"}]

Conclusion: Item listing endpoint functional and correctly integrated with database.