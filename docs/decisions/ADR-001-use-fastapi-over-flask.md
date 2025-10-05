# ADR-001: Use FastAPI over Flask

## Context
The project required a simple yet robust backend API for managing tech products.
The service needed to integrate with:
- **PostgreSQL** as the main database.
- **Nginx** as a reverse proxy and static file server.
- Future observability tools such as **Prometheus** and **Grafana**.

## Decision
We chose **FastAPI** instead of **Flask** for the following reasons:
1. **Type Safety:** FastAPI leverages Pydantic models for strict input/output validation.
2. **Performance:** Built on ASGI, supporting asynchronous requests efficiently.
3. **Documentation:** Auto-generates interactive API docs (`/docs` and `/redoc`).
4. **Developer Experience:** Faster onboarding, less boilerplate, and built-in dependency injection.

## Consequences
- Simplifies development and testing workflows.
- Aligns well with modern async Python stack and Nginx reverse proxy.
- Slight learning curve for developers new to async frameworks.
- Enables easy future integration with Prometheus metrics.