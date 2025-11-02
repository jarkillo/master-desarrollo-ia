# Multi-stage build for AI Dev Academy Frontend
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (dev + prod) for build stage
# TypeScript and Vite are in devDependencies and needed for build
RUN npm ci

# Copy source code
COPY . .

# Build arguments for environment variables
ARG VITE_API_URL
ARG VITE_DEFAULT_PLAYER_ID=1
ARG VITE_ENVIRONMENT=production

# Set environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_DEFAULT_PLAYER_ID=$VITE_DEFAULT_PLAYER_ID
ENV VITE_ENVIRONMENT=$VITE_ENVIRONMENT

# Build the app
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Health check (using curl which is more reliable with IPv4/IPv6)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl --fail --silent --show-error http://127.0.0.1/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
