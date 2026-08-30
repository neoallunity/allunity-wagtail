FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc gettext postgresql-client \
    && rm -rf /var/lib/apt/lists/*
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/production.txt
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
# collectstatic runs at build; provide a placeholder SECRET_KEY (overridden at runtime via env)
ENV SECRET_KEY=build-time-placeholder-not-used-at-runtime
ENV DJANGO_SETTINGS_MODULE=allunity.settings.production
RUN SECRET_KEY=build-time-placeholder python manage.py collectstatic --noinput || true
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "allunity.wsgi:application"]
