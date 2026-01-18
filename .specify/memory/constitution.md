<!--
Sync Impact Report:
Version change: none → 1.0.0
Modified principles: Initial constitution creation
Added sections: All sections (initial creation)
Removed sections: None
Templates requiring updates:
  ✅ plan-template.md - Constitution Check references maintained
  ✅ spec-template.md - Requirements alignment verified
  ✅ tasks-template.md - Task categorization aligned
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All implementation MUST be driven by specifications created in the `specs/` directory. No manual coding is permitted outside of Claude Code execution following spec-driven workflows.

**Rules**:
- Every feature begins with a specification document in `specs/features/[feature-name].md`
- Implementation follows the workflow: Write Spec → Claude Code reads spec → Claude Code implements
- All changes reference their governing spec using `@specs/` notation
- Specs are the single source of truth for requirements, API contracts, and data models
- Claude Code MUST read relevant specs before any implementation work

**Rationale**: Eliminates ambiguity, ensures traceability from requirement to implementation, enables autonomous agent execution with clear boundaries.

### II. Multi-Tenant User Isolation (NON-NEGOTIABLE)

Every API endpoint and database query MUST enforce strict user isolation. No user can access or modify another user's data under any circumstances.

**Rules**:
- All API endpoints extract user ID from verified JWT tokens
- All database queries include user_id filtering in WHERE clauses
- User ID comes exclusively from JWT claims, never from request parameters
- 401 Unauthorized returned for missing/invalid tokens
- 403 Forbidden returned when attempting to access other users' resources
- Database models include user_id foreign key with NOT NULL constraint
- Integration tests MUST verify cross-user isolation

**Rationale**: Security-first design prevents data leakage, satisfies multi-user requirements, provides defense-in-depth through stateless authentication.

### III. JWT Authentication Bridge (NON-NEGOTIABLE)

Authentication uses Better Auth on frontend issuing JWTs, verified by FastAPI backend using shared secret. No session storage, no shared authentication database.

**Rules**:
- Better Auth frontend generates JWT tokens on successful login
- All API requests include `Authorization: Bearer <token>` header
- Backend verifies JWT signature using `BETTER_AUTH_SECRET` environment variable
- Backend extracts user ID from JWT payload (`sub` or `userId` claim)
- Tokens are stateless with embedded expiry (no server-side revocation for MVP)
- Failed verification returns 401 with descriptive error message
- Environment variable `BETTER_AUTH_SECRET` MUST match between frontend and backend

**Rationale**: Stateless authentication enables horizontal scaling, eliminates database round-trips for auth, simplifies frontend-backend contract, standard JWT ecosystem compatibility.

### IV. Monorepo with Clear Boundaries

Project structure separates frontend, backend, and shared specifications with explicit interface contracts.

**Rules**:
- Root `CLAUDE.md` provides high-level project guidance
- `specs/` directory contains all feature specifications, API contracts, database schemas
- `frontend/` contains Next.js application with own `CLAUDE.md` for frontend-specific guidance
- `backend/` contains FastAPI application with own `CLAUDE.md` for backend-specific guidance
- `docker-compose.yml` orchestrates local development environment
- No code sharing between frontend and backend except via API contracts in specs
- Each subdirectory is independently deployable

**Rationale**: Clear separation of concerns, enables parallel frontend/backend development, explicit contracts prevent implicit coupling, supports independent scaling and deployment.

### V. API-First Design

All backend functionality exposed through well-defined REST API endpoints documented in specs before implementation.

**Rules**:
- API contracts defined in `specs/api/rest-endpoints.md` before implementation
- Endpoints follow RESTful conventions: GET (read), POST (create), PUT (update), DELETE (delete), PATCH (partial update)
- All endpoints include user_id in path: `/api/{user_id}/tasks`
- Request/response schemas defined with TypeScript/Python types
- Error responses use standard HTTP status codes with descriptive messages
- API documentation auto-generated from code annotations where possible

**Rationale**: Contract-first approach enables parallel development, facilitates testing, provides clear interface for frontend, enables API versioning strategy.

### VI. Database Schema Integrity

Database schema managed through SQLModel ORM with explicit migrations, type safety, and user scoping.

**Rules**:
- All models defined using SQLModel (Pydantic + SQLAlchemy)
- Every user-specific table includes `user_id` foreign key
- Migrations managed explicitly (Alembic or similar) before deployment
- Database constraints enforce data integrity (NOT NULL, UNIQUE, FOREIGN KEY)
- No raw SQL queries except for complex analytical queries
- Connection pooling configured for production workloads
- Schema documented in `specs/database/schema.md`

**Rationale**: Type-safe ORM prevents runtime errors, migrations enable safe schema evolution, constraints provide database-level validation, documentation ensures schema visibility.

## Technology Stack Constraints

### Frontend Requirements

**Framework**: Next.js 16+ with App Router (NOT Pages Router)
**Language**: TypeScript (strict mode enabled)
**Styling**: Tailwind CSS
**State Management**: React hooks, Context API for global state
**Authentication**: Better Auth library for JWT generation
**API Client**: Native fetch with custom wrapper for token injection

**Justification**: Next.js App Router provides server components for performance, TypeScript eliminates entire classes of bugs, Tailwind enables rapid UI development, Better Auth simplifies JWT flows.

### Backend Requirements

**Framework**: FastAPI (Python 3.13+)
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**Database**: Neon Serverless PostgreSQL
**Authentication**: PyJWT for token verification
**Deployment**: Docker container with Python 3.13-slim base
**Development**: uv for dependency management

**Justification**: FastAPI provides automatic OpenAPI docs and high performance, SQLModel combines ORM with validation, Neon offers serverless PostgreSQL with zero-downtime scaling, PyJWT is industry standard for JWT verification.

### Shared Standards

**Version Control**: Git with conventional commits
**Environment Variables**: `.env.local` files (never committed)
**Secrets Management**: Environment variables for all secrets
**API Documentation**: OpenAPI 3.0 auto-generated from FastAPI
**Logging**: Structured JSON logs for production

## Development Workflow

### Phase-Based Implementation

**Phase I: Specifications** (Complete)
- Console todo app specifications created
- Project structure defined
- Agent roles established

**Phase II: Full-Stack Implementation** (Current)
1. Database schema implementation in backend
2. FastAPI endpoints with JWT verification
3. Next.js frontend with Better Auth integration
4. End-to-end testing of authentication flow
5. Task CRUD operations frontend + backend

**Workflow Steps**:
1. Review spec in `specs/features/[feature].md`
2. Invoke Claude Code: "Implement @specs/features/[feature].md"
3. Claude Code reads root `CLAUDE.md` + feature spec + API spec + database schema + relevant frontend/backend guidance
4. Claude Code implements frontend and backend in parallel
5. Run integration tests to verify behavior
6. Iterate on spec if requirements change

### Spec-Kit Plus Integration

**Commands**:
- `/sp.specify` - Create or update feature specification
- `/sp.plan` - Generate implementation plan from spec
- `/sp.tasks` - Break down plan into actionable tasks
- `/sp.implement` - Execute tasks via Claude Code agents
- `/sp.adr` - Document architectural decisions

**Agent Roles**:
- `spec-intelligence` - Validates and clarifies specifications
- `frontend-app-builder` - Implements Next.js UI and API integration
- `backend-api-builder` - Implements FastAPI endpoints and database operations
- `auth-bridge-verifier` - Ensures JWT authentication correctness
- `database-guardian` - Validates schema integrity and user scoping
- `phase-ii-orchestrator` - Coordinates multi-agent implementation

### Git Workflow

**Branch Strategy**: Feature branches from master
**Commit Messages**: Conventional commits (feat, fix, docs, refactor, test)
**PR Requirements**: All tests pass, spec references included in description
**Code Review**: Automated via Claude Code review agent before merge

## Security Standards

### Authentication Security

- JWTs include expiry (`exp` claim) with reasonable lifetime (1-24 hours)
- Secrets stored in environment variables, never in code
- HTTPS required for all production API traffic
- Token refresh strategy defined before production deployment

### Input Validation

- All user inputs validated on backend (never trust frontend)
- SQL injection prevention via ORM parameterized queries
- XSS prevention via React's automatic escaping
- CSRF protection via SameSite cookies for auth tokens (if cookie-based)

### Data Privacy

- User passwords never stored (Better Auth handles hashing)
- User data isolated per principle II
- No logging of sensitive data (passwords, full tokens)
- Database connections use SSL in production

## Quality Gates

### Before Implementation

- [ ] Feature spec exists in `specs/features/`
- [ ] API contract defined in `specs/api/`
- [ ] Database schema impact assessed in `specs/database/`
- [ ] User isolation verified in spec
- [ ] Authentication requirements explicit

### During Implementation

- [ ] Claude Code reads relevant specs before coding
- [ ] JWT verification included in all protected endpoints
- [ ] User ID filtering applied to all database queries
- [ ] TypeScript types match API contracts
- [ ] Error handling returns appropriate status codes

### Before Deployment

- [ ] All Basic Level features implemented
- [ ] Authentication flow tested end-to-end
- [ ] User isolation verified via integration tests
- [ ] Environment variables documented
- [ ] Docker Compose setup tested locally

## Governance

This constitution is the supreme authority for all development practices in Phase II. Any deviation requires explicit justification documented in an ADR (Architecture Decision Record).

**Amendment Process**:
1. Propose change with rationale
2. Document impact on existing code/specs
3. Update constitution version (semantic versioning)
4. Update dependent templates and specs
5. Create migration plan if breaking changes

**Versioning**:
- MAJOR: Breaking changes to principles (e.g., removing JWT auth, changing monorepo structure)
- MINOR: New principles or significant expansions (e.g., adding new security requirement)
- PATCH: Clarifications, typo fixes, non-semantic refinements

**Compliance**:
- All PRs must verify compliance with constitution
- Agents refuse implementation requests violating principles
- Complexity must be justified if adding beyond defined stack
- Use `CLAUDE.md` at root and subdirectories for runtime guidance

**Constitutional Authority**:
- Constitution overrides conflicting guidance in individual `CLAUDE.md` files
- Agents cite constitution section when rejecting non-compliant requests
- User can override principles only by amending constitution first

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
