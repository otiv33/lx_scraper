FROM postgres:latest AS postgres-db

ENV POSTGRES_DB="sreality"
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="postgres"
ENV POSTGRES_HOST="localhost"

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432