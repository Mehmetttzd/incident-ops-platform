# Incident Ops Platform

Backend-first incident & operations intelligence platform inspired by real-world systems
like PagerDuty and Jira Service Management.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Redis
- Docker Compose

## Features (so far)
- Incident lifecycle with enforced state transitions
- Audit logging for all status changes
- Versioned database schema via migrations
- Clean service-layer business logic

## Status
Phase 1 & 2 complete  
Next: SLA engine + background workers
