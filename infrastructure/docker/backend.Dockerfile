FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY backend/requirements/base.txt /tmp/requirements/base.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements/base.txt

COPY backend /app
RUN chown -R app:app /app

USER app

FROM base AS development

USER root
COPY backend/requirements/development.txt /tmp/requirements/development.txt
RUN pip install -r /tmp/requirements/development.txt
USER app

EXPOSE 8000

FROM base AS production

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]

