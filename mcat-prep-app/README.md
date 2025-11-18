# MCAT Prep Web Application

A comprehensive, user-friendly MCAT preparation web application to help pre-medical students study, practice, and track their progress.

## 🎯 Features

- **Study Material Library**: Organized by MCAT sections (CPBS, CARS, BBLS, PSBB)
- **Practice Question Bank**: 200+ verified questions with detailed explanations
- **Full-Length Practice Tests**: Simulated AAMC MCAT testing experience
- **Progress Analytics**: Track performance by AAMC foundational concepts
- **Concept Mastery Map**: Visual traffic light system (Red/Yellow/Green)
- **Review Queue**: Automatically flag incorrect answers for review
- **Goal Setting**: Set target scores and exam dates

## 🚀 Quick Start (Local Development)

### Prerequisites

- Docker Desktop 4.0+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcat-prep-app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to be healthy** (1-2 minutes)
   ```bash
   docker-compose ps
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

6. **Seed the database with sample data**
   ```bash
   docker-compose exec backend python scripts/seed_database.py
   ```

7. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API Docs: http://localhost:8000/docs
   - Backend Redoc: http://localhost:8000/redoc
   - pgAdmin (optional): http://localhost:5050 (start with `docker-compose --profile debug up`)

### Default Test Account

After seeding, you can log in with:
- **Email**: demo@mcatprep.com
- **Password**: demo123

## 📂 Project Structure

```
mcat-prep-app/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration, security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   └── Dockerfile
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── Dockerfile
├── scripts/               # Database seeds, backups
├── docker-compose.yml     # Local development setup
└── README.md
```

## 🛠️ Development Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
docker-compose down
```

### Reset Database (⚠️ Deletes all data)
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_database.py
```

### Run Backend Tests
```bash
docker-compose exec backend pytest
```

### Create New Database Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
```

### Access PostgreSQL CLI
```bash
docker-compose exec postgres psql -U mcat_user -d mcat_prep
```

### Access Redis CLI
```bash
docker-compose exec redis redis-cli
```

## 📊 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)

### Frontend
- **Framework**: React 18 + TypeScript
- **Routing**: React Router v6
- **State Management**: Zustand + React Query
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Build Tool**: Vite

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx (production)

## 🎓 MCAT Content Structure

### Four Main Sections
1. **CPBS** - Chemical and Physical Foundations of Biological Systems
2. **CARS** - Critical Analysis and Reasoning Skills
3. **BBLS** - Biological and Biochemical Foundations of Living Systems
4. **PSBB** - Psychological, Social, and Biological Foundations of Behavior

### Content Types
- Text summaries and concept reviews
- Flashcards for key terms
- Practice questions (passage-based and standalone)
- Equation sheets and reference materials

## 📈 Analytics Features

- **Score Tracking**: Line charts showing progress over time
- **Concept Mastery**: Heatmap visualization by AAMC foundational concepts
- **Time Analysis**: Average time per question by section
- **Accuracy Trends**: Weekly performance tracking
- **Weak Area Identification**: Personalized study recommendations

## 🔒 Security

- Password hashing with bcrypt
- JWT token-based authentication
- HTTP-only cookies for refresh tokens
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)

## 🚀 Deployment

### Production Deployment Options

1. **AWS** (Recommended for scale)
   - Frontend: S3 + CloudFront
   - Backend: ECS Fargate
   - Database: RDS PostgreSQL
   - Cache: ElastiCache Redis

2. **Vercel + Render** (Easiest)
   - Frontend: Vercel
   - Backend: Render
   - Database: Render PostgreSQL

3. **Self-hosted**
   - Single VPS with Docker Compose
   - Nginx reverse proxy
   - SSL with Let's Encrypt

See deployment documentation for detailed instructions.

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `docker-compose exec backend pytest`
4. Submit a pull request

## 📝 License

Copyright © 2025 MCAT Prep Team. All rights reserved.

## 🆘 Support

For issues or questions:
- Create an issue in the repository
- Email: support@mcatprep.com (placeholder)

## 📅 Development Roadmap

- **Phase I (MVP)** - Q4 2024 - Q2 2025
  - Core study modules (CPBS focus)
  - Question bank (200+ questions)
  - Quiz engine
  - Basic analytics

- **Phase II** - Q3 2025 - Q4 2025
  - All 4 MCAT sections complete
  - Full-length practice tests
  - Advanced analytics
  - Mobile app (React Native)

- **Phase III** - 2026
  - AI-powered adaptive learning
  - Spaced repetition algorithm
  - Community features
  - Premium subscription tiers

---

**Target Launch Date**: November 19, 2025
**Initial User Target**: 100 users
