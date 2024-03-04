#!/bin/bash
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$POSTGRES_DB"  <<-EOSQL
     CREATE TABLE satellite (
          id SERIAL PRIMARY KEY,
          creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          latitude DOUBLE PRECISION,
          longitude DOUBLE PRECISION,
          satellite_id VARCHAR(255) NOT NULL
      );
EOSQL