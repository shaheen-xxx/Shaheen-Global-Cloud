# Shaheen Global Cloud

**A powerful, extensible cloud provisioning platform**

Shaheen Global Cloud is an open-source MVP for provisioning and managing cloud infrastructure. It provides a modern dashboard for creating and managing cloud resources across multiple providers with a unified abstraction layer.

## What is Shaheen Global Cloud?

Shaheen Global Cloud is a cloud provisioning platform that abstracts away provider-specific complexity. Users select their preferred cloud provider, region, and server configuration through a simple web interface, and the platform automatically orchestrates the infrastructure provisioning using OpenTofu.

### Key Features (Phase 1 - MVP)

- ✅ Web Dashboard for server provisioning
- ✅ FastAPI backend with async job processing
- ✅ Redis-based job queue for async provisioning
- ✅ Dagger-based infrastructure execution (isolated, reproducible)
- ✅ OpenTofu infrastructure-as-code
- ✅ Provider abstraction layer (extensible)
- ✅ PostgreSQL for persistence
- ✅ Mock provider for testing
- ✅ Docker Compose for local development
- ✅ GitHub Actions CI/CD pipeline

### Planned Features (Phase 2+)

- Cloudflare Tunnel for HTTPS access
- Multi-cloud support (AWS, DigitalOcean)
- Advanced networking and security groups
- Cost tracking and billing
- Kubernetes support
- Advanced monitoring and observability

## Architecture

```
Frontend (React + TypeScript)
    ↓
FastAPI Backend (Python)
    ↓
Redis Job Queue
    ↓
Worker Process
    ↓
Dagger Module
    ↓
OpenTofu
    ↓
Cloud Provider (Mock/Hetzner/AWS/DO)
    ↓
Ubuntu VM + cloud-init
```

### Component Overview

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React, TypeScript, Vite, Tailwind CSS | User interface for provisioning |
| **Backend** | FastAPI, SQLAlchemy, Pydantic | REST API and business logic |
| **Database** | PostgreSQL | Persistent storage |
| **Queue** | Redis | Async job processing |
| **Execution** | Dagger | Isolated infrastructure automation |
| **IaC** | OpenTofu | Infrastructure definition |
| **Server OS** | Ubuntu 24.04 LTS | Target operating system |

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Local Development

#### 1. Clone the repository

```bash
git clone https://github.com/shaheen-xxx/Shaheen-Global-Cloud.git
cd Shaheen-Global-Cloud
```

#### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 3. Start the development environment

```bash
docker compose up -d
```

Wait for all services to be healthy:

```bash
docker compose ps
```

All services should show `healthy` in the `STATUS` column.

#### 4. Initialize the database

```bash
docker compose exec backend alembic upgrade head
```

#### 5. Create a test user (optional)

```bash
docker compose exec backend python -m app.scripts.create_test_user
```

#### 6. Access the dashboard

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/docs
- **Database**: postgres://localhost:5432 (shaheen:shaheen_password)

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://shaheen:...@postgres:5432/shaheen_cloud` | PostgreSQL connection string |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection string |
| `FASTAPI_ENV` | `development` | Environment (development/production) |
| `FASTAPI_DEBUG` | `true` | Enable debug mode |
| `SECRET_KEY` | `dev-secret-key-...` | JWT signing key (change in production) |
| `LOG_LEVEL` | `DEBUG` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `VITE_API_URL` | `http://localhost:8000/api` | Backend API URL for frontend |

## Running Services Individually

### Backend API

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Worker Process

```bash
cd backend
source venv/bin/activate
python -m app.worker
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running OpenTofu Operations

```bash
cd infrastructure
tofu init
tofu validate
tofu plan -var-file=environments/production/terraform.tfvars
```

## API Documentation

### Create Server

```http
POST /api/v1/servers
Content-Type: application/json

{
  "name": "ubuntu-01",
  "provider": "mock",
  "region": "fsn1",
  "size": "cx22",
  "image": "ubuntu-24.04"
}
```

**Response** (202 Accepted):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "server_id": "123",
  "status": "PENDING"
}
```

### Get Server

```http
GET /api/v1/servers/{id}
```

### List Servers

```http
GET /api/v1/servers
```

### Get Job Status

```http
GET /api/v1/jobs/{job_id}
```

### Get Server Logs

```http
GET /api/v1/servers/{server_id}/logs
```

### Destroy Server

```http
POST /api/v1/servers/{id}/destroy
```

### Health Check

```http
GET /api/v1/health
```

## Testing

### Backend Tests

```bash
docker compose exec backend pytest
```

### Frontend Build

```bash
docker compose exec frontend npm run build
```

### OpenTofu Validation

```bash
docker compose exec backend python -m app.scripts.validate_tofu
```

### Dagger Module Validation

```bash
cd dagger
dagger develop
```

## Security Model

### What We Protect

- **Credentials**: Cloud provider credentials are never stored in Git, committed to database plaintext, or logged
- **Secrets**: All secrets are injected via environment variables or secret management systems
- **User Input**: Only JSON specifications are accepted; no arbitrary HCL or shell commands
- **Execution Isolation**: Dagger provides isolated, reproducible execution
- **State Files**: Terraform/OpenTofu state files are never committed to Git

### What We Don't Do

- ❌ Hard-coded credentials in code
- ❌ Credentials in Git history
- ❌ User-supplied OpenTofu HCL
- ❌ Shell execution from user input
- ❌ Running backend as root
- ❌ Logging credentials

### Best Practices

1. Use `.env.example` for template variables only
2. Store real credentials in environment variables or a secret manager
3. Use `.gitignore` to prevent accidental commits
4. Rotate credentials regularly
5. Use IAM roles when running on cloud providers
6. Enable audit logging
7. Review provisioned resources regularly

## Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs

# Check specific service
docker compose logs backend

# Restart services
docker compose restart
```

### Database connection errors

```bash
# Check PostgreSQL is running
docker compose exec postgres pg_isready

# Check database exists
docker compose exec postgres psql -U shaheen -c "\l"
```

### Redis connection errors

```bash
# Check Redis is running
docker compose exec redis redis-cli ping
```

### Frontend not connecting to backend

- Check `VITE_API_URL` in `.env`
- Verify backend is running: `curl http://localhost:8000/api/v1/health`
- Check browser console for CORS errors

### Worker not processing jobs

```bash
# Check worker logs
docker compose logs worker

# Check Redis has jobs
docker compose exec redis redis-cli LLEN "provisioning:queue"
```

## Project Structure

```
Shaheen-Global-Cloud/
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app setup
│   │   ├── config.py             # Configuration
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── worker.py             # Job worker
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── endpoints/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── servers.py
│   │   │       │   ├── jobs.py
│   │   │       │   └── health.py
│   │   │       └── schemas.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── models.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── server_service.py
│   │   │   ├── job_service.py
│   │   │   ├── provider_service.py
│   │   │   └── dagger_service.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── mock.py
│   │   │   └── hetzner.py
│   │   ├── queue/
│   │   │   ├── __init__.py
│   │   │   └── job_queue.py
│   │   └── scripts/
│   │       ├── __init__.py
│   │       └── create_test_user.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_health.py
│   │   ├── test_servers.py
│   │   ├── test_providers.py
│   │   └── test_jobs.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pytest.ini
├── frontend/                     # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── CreateServerForm.tsx
│   │   │   ├── ServerList.tsx
│   │   │   ├── ServerDetails.tsx
│   │   │   └── ProvisioningProgress.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── ServersPage.tsx
│   │   │   └── ServerDetailPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   ├── styles/
│   │   │   └── globals.css
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── dagger/                       # Dagger module
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── infrastructure/               # OpenTofu configuration
│   ├── modules/
│   │   └── ubuntu-vm/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   ├── environments/
│   │   └── production/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       ├── outputs.tf
│   │       ├── versions.tf
│   │       └── terraform.tfvars.example
│   └── .terraformignore
├── scripts/                      # Utility scripts
│   ├── setup.sh
│   ├── test.sh
│   └── validate.sh
├── .github/
│   └── workflows/
│       └── test.yml
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Workflow: Server Provisioning

1. **User creates server request** via dashboard
2. **Frontend sends** `POST /api/v1/servers` with server configuration
3. **Backend validates** request and creates Server + ProvisioningJob records
4. **Backend returns** job_id immediately (202 Accepted)
5. **Worker listens** to Redis job queue
6. **Worker dequeues** job and updates status to PROVISIONING
7. **Worker calls** Dagger module with infrastructure config
8. **Dagger container** is spawned in isolation
9. **Dagger runs** `tofu init`, `tofu validate`, `tofu plan`, `tofu apply`
10. **OpenTofu executes** against cloud provider
11. **Provider creates** Ubuntu VM and returns IPv4
12. **cloud-init** runs on VM, installing packages and preparing system
13. **Worker updates** Server status to BOOTSTRAPPING
14. **Worker waits** for cloud-init completion (health checks)
15. **Server status** changes to READY
16. **Frontend polls** `/api/v1/servers/{id}` and displays updated status

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

### Phase 1 (Current)
- [x] MVP with mock provider
- [x] Basic authentication
- [x] Server provisioning workflow
- [x] Job queue and worker
- [x] Dagger integration
- [x] OpenTofu integration

### Phase 2
- [ ] Cloudflare Tunnel integration
- [ ] Additional cloud providers (AWS, DigitalOcean)
- [ ] Advanced networking
- [ ] Security groups and firewall rules
- [ ] SSH key management

### Phase 3
- [ ] Billing and cost tracking
- [ ] Advanced monitoring
- [ ] Kubernetes support
- [ ] Auto-scaling
- [ ] Multi-region deployments

## License

MIT License - see [LICENSE](LICENSE) for details

## Support

- 📧 Email: support@shaheen.cloud
- 💬 Discussions: https://github.com/shaheen-xxx/Shaheen-Global-Cloud/discussions
- 🐛 Issues: https://github.com/shaheen-xxx/Shaheen-Global-Cloud/issues

---

**Made with ❤️ by Shaheen Global**
