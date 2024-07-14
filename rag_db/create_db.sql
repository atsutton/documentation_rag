-- Functions
CREATE OR REPLACE FUNCTION set_CreatedDate() RETURNS TRIGGER AS $$
BEGIN
    NEW."CreatedDate" = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_LastModifiedDate() RETURNS TRIGGER AS $$
BEGIN
    NEW."LastModifiedDate" = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    user_name TEXT = 'rag_user';
    user_password TEXT = 'rag_user';
    db_name TEXT = 'rag_db';
    db_table_name TEXT = 'rag_logs';
    trigger_created_date TEXT = db_table_name || '_setCreatedDate';
    trigger_modified_date TEXT = db_table_name || '_setLastModifiedDate';
BEGIN
    -- Database
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = db_name) THEN
        EXECUTE format('CREATE DATABASE %I', db_name);
    ELSE
        RAISE NOTICE 'Database % already exists, skipping creation.', db_name;
    END IF;

    -- User
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = user_name) THEN
        EXECUTE format('CREATE USER %I WITH PASSWORD %L', user_name, user_password);
    ELSE
        RAISE NOTICE 'User % already exists, skipping creation.', user_name;
    END IF;

    -- Permissions
    EXECUTE format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I', db_name, user_name);

    -- Table
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = db_table_name) THEN
        EXECUTE format('
            CREATE TABLE %I (
                "UserInput" TEXT,
                "SubqueriesRequest" TEXT,
                "SubqueriesResponse" TEXT,
                "EmbeddingsUnique" TEXT,
                "EmbeddingsScored" TEXT,
                "EmbeddingsTop" TEXT,
                "MainRequest" TEXT,
                "MainResponse" TEXT,
                "Id" SERIAL PRIMARY KEY,
                "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "LastModifiedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "IsSuccess" BOOLEAN,
                "ErrorMessage" TEXT
            )
        ', db_table_name);
    ELSE
        RAISE NOTICE 'Table % already exists, skipping creation.', db_table_name;
    END IF;

    -- Triggers
    EXECUTE format('
        CREATE OR REPLACE TRIGGER %I 
        BEFORE INSERT ON %I 
        FOR EACH ROW EXECUTE FUNCTION set_CreatedDate();
    ', trigger_created_date, db_table_name);

    EXECUTE format('
        CREATE OR REPLACE TRIGGER %I 
        BEFORE INSERT OR UPDATE ON %I 
        FOR EACH ROW EXECUTE FUNCTION set_LastModifiedDate();
    ', trigger_modified_date, db_table_name);

END $$;