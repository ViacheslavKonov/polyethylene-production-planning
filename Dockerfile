FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/srv/app
WORKDIR /srv/app
LABEL org.opencontainers.image.source="https://github.com/ViacheslavKonov/polyethylene-production-planning"
COPY pyproject.toml ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY scripts/entrypoint.sh ./scripts/entrypoint.sh
RUN pip install --no-cache-dir .
RUN chmod +x ./scripts/entrypoint.sh && useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /srv/app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["./scripts/entrypoint.sh"]
