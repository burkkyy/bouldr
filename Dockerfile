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

# Stage 3 - Production
FROM python:3.11.2-slim

RUN apt-get update

ARG RELEASE_TAG
ARG GIT_COMMIT_HASH

ENV RELEASE_TAG=${RELEASE_TAG}
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}
ENV NODE_ENV=production
ENV TZ=UTC

WORKDIR /root/app

COPY api ./
RUN rm -r .venv

COPY --from=web-build-stage /usr/src/web/dist ./src/web/

RUN echo "RELEASE_TAG=${RELEASE_TAG}" >> VERSION
RUN echo "GIT_COMMIT_HASH=${GIT_COMMIT_HASH}" >> VERSION

EXPOSE 5000

RUN chmod +x ./bin/boot-app.sh

CMD ["./bin/boot-app.sh"]