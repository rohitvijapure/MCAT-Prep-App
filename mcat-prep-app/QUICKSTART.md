# MCAT Prep - Quick Start Guide

This guide will help you get the MCAT Prep application running locally using Docker in just a few minutes.

## 🚀 Prerequisites

Before you begin, ensure you have:

- **Docker Desktop 4.0+** installed and running
  - Download from: https://www.docker.com/products/docker-desktop
- **Git** (for cloning the repository)

That's it! Docker will handle all other dependencies.

## 📦 Installation Steps

### 1. Navigate to the Project Directory

```bash
cd /home/user/Python/mcat-prep-app
```

### 2. Set Up Environment Variables

The `.env.local` file has already been created with default development settings. For production, you should change these values.

```bash
# View the environment file
cat .env.local
```

### 3. Start All Services with Docker Compose

This single command will:
- Build Docker images for backend and frontend
- Start PostgreSQL database
- Start Redis cache
- Start the FastAPI backend (port 8000)
- Start the React frontend (port 5173)

```bash
docker-compose up -d
```

**First-time build may take 3-5 minutes.** Subsequent starts will be much faster.

### 4. Check Service Status

Wait for all services to be healthy (usually 1-2 minutes):

```bash
docker-compose ps
```

You should see all services with status "Up" or "Up (healthy)".

### 5. Initialize the Database

Run database migrations and seed with initial data:

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed database with sample data
docker-compose exec backend python scripts/seed_database.py
```

Or use the convenience script:

```bash
./scripts/init_db.sh
```

### 6. Access the Application

Once everything is running, open your browser to:

- **Frontend Application**: http://localhost:5173
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc

### 7. Login with Demo Account

Use these credentials to log in:

- **Email**: `demo@mcatprep.com`
- **Password**: `demo123`

## 🎉 You're All Set!

The application is now running locally. You can:

- View the dashboard with analytics
- Create custom quizzes
- Browse study materials
- Track your progress

## 🛠️ Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### Reset Database (⚠️ Deletes all data)

```bash
docker-compose down -v
docker-compose up -d
./scripts/init_db.sh
```

### Access PostgreSQL Database

```bash
docker-compose exec postgres psql -U mcat_user -d mcat_prep
```

### Access Python Shell in Backend

```bash
docker-compose exec backend python
```

### Run Backend Tests

```bash
docker-compose exec backend pytest
```

### Rebuild After Code Changes

If you make changes to dependencies or Dockerfiles:

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## 📝 Development Workflow

### Backend Development

1. Edit files in `backend/app/`
2. FastAPI will auto-reload (hot reload enabled)
3. View changes immediately at http://localhost:8000

### Frontend Development

1. Edit files in `frontend/src/`
2. Vite will auto-reload (hot reload enabled)
3. View changes immediately at http://localhost:5173

### Database Schema Changes

1. Modify models in `backend/app/models/`
2. Create migration:
   ```bash
   docker-compose exec backend alembic revision --autogenerate -m "description"
   ```
3. Apply migration:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## 🔍 Troubleshooting

### Port Already in Use

If you get port conflicts:

```bash
# Check what's using the port
lsof -i :5173  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# Stop the conflicting service or change ports in docker-compose.yml
```

### Services Not Starting

```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Try rebuilding
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Error

```bash
# Wait for PostgreSQL to be fully ready
docker-compose exec postgres pg_isready -U mcat_user

# Check database exists
docker-compose exec postgres psql -U mcat_user -l
```

### Frontend Can't Connect to Backend

1. Check backend is running: http://localhost:8000/health
2. Verify CORS settings in `backend/app/core/config.py`
3. Check `.env.local` has correct `VITE_API_URL=http://localhost:8000`

## 📊 Next Steps

### Add Real MCAT Content

The current seed data has only 5 sample questions. To build a comprehensive prep platform:

1. **Research MCAT Content**: Use official AAMC resources
2. **Create Questions**: Add to `scripts/seed_database.py` or create import scripts
3. **Add Study Modules**: Create comprehensive text, videos, flashcards
4. **Review for Accuracy**: Ensure all content is medically and scientifically accurate

### Extend Functionality

The MVP includes basic features. Consider adding:

- Full-length practice tests
- Timed quiz mode with countdown
- Detailed answer explanations with images
- Flashcard system
- Spaced repetition algorithm
- Progress tracking charts
- Export progress reports
- Mobile app (React Native)

### Deploy to Production

When ready to deploy:

1. See `README.md` for deployment options (AWS, Vercel, etc.)
2. Change all secrets in `.env`
3. Set up SSL certificates
4. Configure backups
5. Set up monitoring (Sentry, CloudWatch)

## 💬 Support

For issues or questions:
- Check the main README.md for detailed documentation
- Review Docker logs for error messages
- Ensure all prerequisites are installed correctly

## 🎯 Current Status

**✅ Completed Features:**
- User authentication (register, login, JWT)
- Database models for all entities
- Question bank with 5 sample questions
- Quiz generation API
- Basic analytics dashboard
- User progress tracking
- Review queue system

**🚧 In Progress:**
- Full MCAT content (200+ questions needed)
- Advanced analytics visualizations
- Full-length practice test interface

**📅 Launch Date: November 19, 2025**

---

Happy studying! 📚🎓
