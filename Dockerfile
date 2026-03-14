# Stage 1 - Build web for production
FROM node:23.2.0-alpine3.20 AS web-build-stage

ENV NODE_ENV=development

WORKDIR /usr/src/web

COPY web/package*.json ./
COPY web/tsconfig*.json ./
COPY web/vite.config.js ./
RUN npm install

COPY web ./

# Switching to production mode for build environment.
ENV NODE_ENV=production
RUN npm run build

# Stage 2 - Build API
FROM python:3.11.2-slim AS api-build-stage

RUN apt-get update

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /usr/src/api

ENV NODE_ENV=production

COPY api ./
RUN uv sync --frozen

# Being lazy and moving production only code manually
RUN mkdir -p dist/src
RUN mv src/blueprints ./dist/src/
RUN mv src/models ./dist/src/
RUN mv src/services ./dist/src/
RUN mv src/__init__.py ./dist/src/
RUN mv src/app.py ./dist/src/
RUN mv src/config.py ./dist/src/

RUN mv pyproject.toml ./dist/
RUN mv uv.lock ./dist/
RUN mv .venv ./dist/

# Stage 3 - Production
FROM python:3.11.2-slim

RUN apt-get update

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG RELEASE_TAG
ARG GIT_COMMIT_HASH

ENV RELEASE_TAG=${RELEASE_TAG}
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}
ENV NODE_ENV=production
ENV TZ=UTC

WORKDIR /root/app

COPY --from=api-build-stage /usr/src/api/dist ./dist/
COPY --from=web-build-stage /usr/src/web/dist ./dist/src/web/

RUN echo "RELEASE_TAG=${RELEASE_TAG}" >> VERSION
RUN echo "GIT_COMMIT_HASH=${GIT_COMMIT_HASH}" >> VERSION

EXPOSE 5000

COPY --from=api-build-stage /usr/src/api/bin/boot-app.sh ./bin/boot-app.sh
RUN chmod +x ./bin/boot-app.sh

CMD ["./bin/boot-app.sh"]