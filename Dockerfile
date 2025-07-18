# Multi-stage build for the entire MSA project
# This Dockerfile can be used to build all services in a single container
# For production, it's recommended to use docker-compose with individual Dockerfiles

FROM node:18-alpine AS frontend-builder

# Install pnpm globally
RUN npm install -g pnpm

# Build Frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN pnpm config set store-dir /tmp/.pnpm-store
RUN pnpm install --frozen-lockfile --unsafe-perm
COPY frontend/ ./
RUN pnpm run build

FROM python:3.12-slim AS backend-builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Build Gateway Service
WORKDIR /app/gateway
COPY gateway/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY gateway/ ./

# Build Auth Service
WORKDIR /app/auth-service
COPY auth-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY auth-service/ ./

# Final stage - Runtime
FROM python:3.12-slim AS runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and pnpm for frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm

# Create app directory
WORKDIR /app

# Copy built applications
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /app/frontend/
COPY --from=frontend-builder /app/frontend/pnpm-lock.yaml* /app/frontend/
COPY --from=frontend-builder /app/frontend/next.config.js /app/frontend/

COPY --from=backend-builder /app/gateway /app/gateway
COPY --from=backend-builder /app/auth-service /app/auth-service

# Install frontend dependencies
WORKDIR /app/frontend
RUN pnpm config set store-dir /tmp/.pnpm-store
RUN pnpm install --frozen-lockfile --prod --unsafe-perm

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app

# Expose ports
EXPOSE 3000 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health && \
      curl -f http://localhost:8001/health && \
      curl -f http://localhost:3000 || exit 1

# Start all services with supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"] 