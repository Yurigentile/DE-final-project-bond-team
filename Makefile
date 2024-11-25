# Database connection variables
DB_NAME = test_database
DB_USER = test_user
DB_HOST = localhost
DB_PORT = 5432
ADMIN_DB = postgres
PGPASSWORD = test

# SQL files for table creation and test data
CREATE_TABLES_FILE = db_sql/create_tables.sql
INSERT_DATA_FILE = db_sql/insert_data.sql

# Default rule to run all steps
.PHONY: all
all: create-env-file create-user drop-create-db setup-tables insert-data

# Rule to create the .env.test file
.PHONY: create-env-file
create-env-file:
	@echo "Creating .env.test file..."
	@echo "DB_NAME=$(DB_NAME)" > .env.test
	@echo "DB_USER=$(DB_USER)" >> .env.test
	@echo "DB_HOST=$(DB_HOST)" >> .env.test
	@echo "DB_PORT=$(DB_PORT)" >> .env.test
	@echo "DB_PASSWORD=$(PGPASSWORD)" >> .env.test
	@echo ".env.test file created successfully."

# Rule to create the test user if it doesn't exist
.PHONY: create-user
create-user:
	@echo "Creating user $(DB_USER) if it doesn't exist..."
	@USER_EXISTS=$$(psql -h $(DB_HOST) -p $(DB_PORT) -U postgres -d $(ADMIN_DB) -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$(DB_USER)'"); \
	if [ -z "$$USER_EXISTS" ]; then \
		psql -h $(DB_HOST) -p $(DB_PORT) -U postgres -d $(ADMIN_DB) -c "CREATE ROLE $(DB_USER) LOGIN PASSWORD '$(PGPASSWORD)';"; \
		echo "User $(DB_USER) created successfully."; \
	else \
		echo "User $(DB_USER) already exists."; \
	fi

# Rule to drop the database if it exists and create it
.PHONY: drop-create-db
drop-create-db:
	@echo "Dropping database $(DB_NAME) if it exists..."
	PGPASSWORD=$(PGPASSWORD) psql -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) -d $(ADMIN_DB) -c "DROP DATABASE IF EXISTS $(DB_NAME);"
	@echo "Creating database $(DB_NAME)..."
	PGPASSWORD=$(PGPASSWORD) psql -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) -d $(ADMIN_DB) -c "CREATE DATABASE $(DB_NAME);"
	@echo "Database $(DB_NAME) created successfully."

# Rule to create tables
.PHONY: setup-tables
setup-tables: $(CREATE_TABLES_FILE)
	@echo "Creating tables in $(DB_NAME)..."
	PGPASSWORD=$(PGPASSWORD) psql -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) -d $(DB_NAME) -f $(CREATE_TABLES_FILE)
	@echo "Tables created successfully."

# Rule to insert test data
.PHONY: insert-data
insert-data: $(INSERT_DATA_FILE)
	@echo "Inserting test data into $(DB_NAME)..."
	PGPASSWORD=$(PGPASSWORD) psql -h $(DB_HOST) -p $(DB_PORT) -U $(DB_USER) -d $(DB_NAME) -f $(INSERT_DATA_FILE)
	@echo "Test data inserted successfully."