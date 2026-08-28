# Stage 1: Build the Python application using uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS python-builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

ADD . /code

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


# Stage 2: Build the frontend files
FROM node:23-bookworm-slim AS node-builder
WORKDIR /code

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build


# Stage 3: Final image
FROM python:3.12-slim-bookworm

ENV PATH="/code/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
ENV DJANGO_SETTINGS_MODULE=core.settings_production

RUN apt-get update \
    && apt-get install -y curl libpq-dev \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=python-builder /code /code
COPY --from=node-builder /code/frontend/dist /code/frontend/dist
COPY . /code

RUN mkdir -p media logs static

COPY docker_startup.sh /start
RUN chmod +x /start

CMD ["/start"]
