#!/bin/bash
psql -U postgres -d delphi  -f ./$1.sql
echo "Database updated successfully."