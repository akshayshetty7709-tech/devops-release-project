FROM python:3.12-slim

WORKDIR /app
COPY app.py .

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

RUN useradd -m appuser
USER appuser

EXPOSE 8080
CMD ["python", "app.py"]
