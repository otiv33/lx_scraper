FROM postgres:latest AS postgres-db

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432