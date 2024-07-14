FROM postgres:15

WORKDIR /app

ENV POSTGRES_USER=postgres

COPY create_db.sql /docker-entrypoint-initdb.d/create_db.sql

EXPOSE 5432