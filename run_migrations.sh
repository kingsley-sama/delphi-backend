#!/bin/bash
# Database migration script for Delphi Backend

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Delphi Database Migration${NC}"
echo "=============================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Load environment variables
source .env

# Extract database connection details from DATABASE_URL
# Format: postgresql+asyncpg://user:password@host:port/database
DB_URL_SYNC=$(echo $DATABASE_URL | sed 's/+asyncpg//')

echo "Running migration: migrations/001_initial_schema.sql"
echo "----------------------------"

# Run the migration
psql $DB_URL_SYNC -f migrations/001_initial_schema.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migration completed successfully${NC}"
else
    echo -e "${RED}✗ Migration failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Database setup complete!${NC}"
