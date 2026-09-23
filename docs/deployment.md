# Deployment & Production Setup

## Docker Deployment

Build and run the containerized backend:
```bash
cd backend
docker build -t alertx2-backend:latest .
docker run -d -p 8000:8000 --env-file ../.env alertx2-backend:latest
```

## Production PostgreSQL & Redis

Update `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/alertx2_prod
REDIS_URL=redis://localhost:6379/0
DEBUG=False
SECRET_KEY=<generate-strong-key>
```

Run database migrations:
```bash
alembic upgrade head
```
