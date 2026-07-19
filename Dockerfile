
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /my-project-service

COPY .  .

RUN uv sync

ENV PATH="/my-project-service/.venv/bin:$PATH"

CMD ["fastapi","run","main.py"]