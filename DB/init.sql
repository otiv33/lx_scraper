DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sreality') THEN
      CREATE DATABASE sreality;
   END IF;
END $$;


CREATE TABLE IF NOT EXISTS apartments (
    id SERIAL PRIMARY KEY, 
    title VARCHAR(255), 
    image VARCHAR(255)
);